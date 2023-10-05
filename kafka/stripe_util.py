import stripe
from decouple import config


def stripeUtil(event, name, email):
    stripe.api_key = config("STRIPE_SECRET_KEY")

    customer = stripe.Customer.list(email=email)

    if event == "user_deleted":
        customer_id = customer["data"][0]["id"]
        stripe.Customer.delete(customer_id)
        print(f"Deleted customer: {customer_id}")

    elif event == "user_updated":
        customer_id = customer["data"][0]["id"]
        stripe.Customer.modify(
            customer_id,
            name=name,
            email=email,
        )
        print(f"Updated customer: {customer_id}")
 
    elif event == "user_created":
        if len(customer["data"]) == 0:
            customer = stripe.Customer.create(
                name=name,
                email=email,
            )
            print(f"Created customer: {customer.id}")
