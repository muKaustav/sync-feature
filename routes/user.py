from fastapi import APIRouter, Request
from sqlalchemy.orm import Session
from config.db import conn
from models.user import users
from schemas.user import User, PartialUser
from kafka.kafka_producer import produce_message
from starlette.responses import JSONResponse
import json

user = APIRouter()


@user.get("/")
def get_users():
    try:
        with Session(bind=conn) as db:
            result_proxy = db.execute(users.select())
            rows = result_proxy.fetchall()

            column_names = result_proxy.keys()

            data = [dict(zip(column_names, row)) for row in rows]

            response = {"status": "OK", "data": data}
            return JSONResponse(content=response, status_code=200)

    except Exception as e:
        print(e)
        response = {"status": "ERROR", "message": "Unable to fetch users."}
        return JSONResponse(content=response, status_code=500)


@user.post("/")
def create_user(user: User):
    try:
        with Session(bind=conn) as db:
            new_user = {"name": user.name, "email": user.email}

            result = db.execute(users.insert().values(new_user))

            print(result)

            db.commit()

            kafka_message = {
                "event": "user_created",
                "user": new_user,
            }

            produce_message(
                "user-events",
                key="outward-sync",
                value=json.dumps(kafka_message),
            )

            response = {"status": "OK", "message": "User created successfully."}
            return JSONResponse(content=response, status_code=201)

    except Exception as e:
        print(e)

        if "duplicate key value violates unique constraint" in str(e):
            response = {
                "status": "ERROR",
                "message": "User with this email already exists.",
            }
            return JSONResponse(content=response, status_code=400)

        response = {"status": "ERROR", "message": "Unable to create user."}
        return JSONResponse(content=response, status_code=500)


@user.get("/{id}")
def get_user(id: str):
    try:
        with Session(bind=conn) as db:
            if not id.isdigit():
                response = {
                    "status": "ERROR",
                    "message": "Invalid user id. Please provide a valid integer.",
                }

                return JSONResponse(content=response, status_code=400)

            result_proxy = db.execute(
                users.select().where(users.c.id == int(id))
            ).first()

            if result_proxy:
                column_names = users.c.keys()

                data = dict(zip(column_names, result_proxy))

                response = {"status": "OK", "data": data}
                return JSONResponse(content=response, status_code=200)

            else:
                response = {"status": "ERROR", "message": "User not found."}
                return JSONResponse(content=response, status_code=404)

    except Exception as e:
        print(e)
        response = {"status": "ERROR", "message": "Unable to fetch user."}
        return JSONResponse(content=response, status_code=500)


@user.put("/{id}")
def update_user(id: str, user_update: PartialUser):
    try:
        with Session(bind=conn) as db:
            if not id.isdigit():
                response = {
                    "status": "ERROR",
                    "message": "Invalid user id. Please provide a valid integer.",
                }
                return JSONResponse(content=response, status_code=400)

            user = db.query(users).filter(users.c.id == int(id)).first()

            if user is None:
                response = {"status": "ERROR", "message": "User not found."}
                return JSONResponse(content=response, status_code=404)

            if user_update.name is not None:
                db.query(users).filter(users.c.id == int(id)).update(
                    {"name": user_update.name}
                )

            db.commit()

            updated_user = db.query(users).filter(users.c.id == int(id)).first()

            if updated_user is None:
                response = {"status": "ERROR", "message": "Updated user not found."}
                return JSONResponse(content=response, status_code=404)

            kafka_message = {
                "event": "user_updated",
                "user": {
                    "id": updated_user.id,
                    "name": updated_user.name,
                    "email": updated_user.email,
                },
            }

            produce_message(
                "user-events",
                key="outward-sync",
                value=json.dumps(kafka_message),
            )

            response = {
                "status": "OK",
                "message": "User updated successfully.",
                "updated_user": {
                    "id": updated_user.id,
                    "name": updated_user.name,
                    "email": updated_user.email,
                },
            }
            
            return JSONResponse(content=response, status_code=200)

    except Exception as e:
        print(e)
        response = {"status": "ERROR", "message": "Unable to update user."}
        return JSONResponse(content=response, status_code=500)


@user.delete("/{id}")
def delete_user(id: str):
    try:
        with Session(bind=conn) as db:
            if not id.isdigit():
                response = {
                    "status": "ERROR",
                    "message": "Invalid user id. Please provide a valid integer.",
                }

                return JSONResponse(content=response, status_code=400)

            to_delete = db.execute(users.select().where(users.c.id == int(id))).first()

            email = to_delete[2]
            name = to_delete[1]

            result = db.execute(users.delete().where(users.c.id == int(id)))

            if result.rowcount == 0:
                response = {"status": "ERROR", "message": "User not found."}
                return JSONResponse(content=response, status_code=404)

            db.commit()

            kafka_message = {
                "event": "user_deleted",
                "user": {"id": id, "email": email, "name": name},
            }

            produce_message(
                "user-events",
                key="outward-sync",
                value=json.dumps(kafka_message),
            )

            response = {"status": "OK", "message": "User deleted successfully."}
            return JSONResponse(content=response, status_code=200)

    except Exception as e:
        print(e)
        response = {"status": "ERROR", "message": "Unable to delete user."}
        return JSONResponse(content=response, status_code=500)


@user.post("/sync")
async def inward_sync(request: Request):
    try:
        payload = await request.json()
        print(payload)

        updated_name = payload["data"]["object"]["name"]
        email_to_update = payload["data"]["object"]["email"]

        user_dict = {
            "email": email_to_update,
            "name": updated_name,
        }

        kafka_message = {"event": "inward-sync", "user": user_dict}

        produce_message(
            "stripe-events",
            key="inward-sync",
            value=json.dumps(kafka_message),
        )

        response = {"status": "OK", "message": "Syncing with Stripe."}
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        print(e)
        response = {"status": "ERROR", "message": "Unable to sync with Stripe."}
        return JSONResponse(content=response, status_code=500)
