import stripe
from decouple import config
from datetime import datetime
from sqlalchemy.orm import Session
from decouple import config
from sqlalchemy.orm import Session
from models.user import users
from config.db import conn


stripe.api_key = config("STRIPE_SECRET_KEY")


def stripeOutwardSyncUtil(event, name, email):
    try:
        customer = stripe.Customer.list(email=email)

        if event == "user_deleted":
            customer_id = customer["data"][0]["id"]

            try:
                stripe.Customer.delete(customer_id)

                logs = {
                    "message": f"Deleted customer: {customer_id}",
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)

            except Exception as e:
                logs = {
                    "message": f"Customer {customer_id} not found.",
                    "error": e,
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)
                return

        elif event == "user_updated":
            customer_id = customer["data"][0]["id"]

            try:
                stripe.Customer.modify(
                    customer_id,
                    name=name,
                    email=email,
                )

                logs = {
                    "message": f"Updated customer: {customer_id}",
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)

            except Exception as e:
                logs = {
                    "message": f"Customer {customer_id} not found.",
                    "error": e,
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)
                return

        elif event == "user_created":
            try:
                if len(customer["data"]) == 0:
                    customer = stripe.Customer.create(
                        name=name,
                        email=email,
                    )

                    logs = {
                        "message": f"Created customer: {customer['id']}",
                        "timestamp": datetime.now().timestamp(),
                    }

                    print(logs)

            except Exception as e:
                logs = {
                    "message": f"Customer {email} already exists.",
                    "error": e,
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)
                return

    except Exception as e:
        logs = {
            "message": f"Customer {email} not found.",
            "error": e,
            "timestamp": datetime.now().timestamp(),
        }

        print(logs)
        return


def stripeInwardSyncUtil(email, name, event):
    try:
        with Session(bind=conn) as db:
            if event == "customer.created":
                try:
                    result = db.execute(users.insert().values(name=name, email=email))

                    if result.rowcount == 0:
                        logs = {
                            "message": f"User {email} already exists.",
                            "timestamp": datetime.now().timestamp(),
                        }

                        print(logs)
                        return

                except Exception as e:
                    logs = {
                        "message": f"Synced with Stripe.",
                        "timestamp": datetime.now().timestamp(),
                    }

                    print(logs)
                    return

                logs = {
                    "message": f"Created user: {email}",
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)

            elif event == "customer.deleted":
                try:
                    result = db.execute(users.delete().where(users.c.email == email))

                    if result.rowcount == 0:
                        logs = {
                            "message": f"User {email} not found.",
                            "timestamp": datetime.now().timestamp(),
                        }

                        print(logs)
                        return

                except Exception as e:
                    logs = {
                        "message": f"Synced with Stripe.",
                        "timestamp": datetime.now().timestamp(),
                    }

                    print(logs)
                    return

                logs = {
                    "message": f"Deleted user: {email}",
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)

            else:
                result = db.execute(
                    users.update().where(users.c.email == email).values(name=name)
                )

                if result.rowcount == 0:
                    logs = {
                        "message": f"User {email} not found.",
                        "timestamp": datetime.now().timestamp(),
                    }

                    print(logs)
                    return

                logs = {
                    "message": f"Synced with Stripe for user: {email}",
                    "timestamp": datetime.now().timestamp(),
                }

                print(logs)

            db.commit()

    except Exception as e:
        logs = {
            "message": f"Error creating/updating user: {email}",
            "error": e,
            "timestamp": datetime.now().timestamp(),
        }

        print(logs)
        return
