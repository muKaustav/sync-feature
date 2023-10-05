import json
from decouple import config
from stripe_util import stripeUtil
from confluent_kafka import Consumer, KafkaError

kafka_config = {
    "bootstrap.servers": f'{config("HOST_IP")}:9092',
    "group.id": "my-consumer-group",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(kafka_config)

consumer.subscribe(["user-events", "stripe-events"])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("Reached end of partition")
            else:
                print(f"Error: {msg.error()}")

        else:
            key = msg.key()
            value = msg.value()

            print(f"Received message: Key={key}, Value={value}")

            if key == b"outward-sync":
                name = json.loads(value)["user"]["name"]
                email = json.loads(value)["user"]["email"]
                event = json.loads(value)["event"]

                stripeUtil(event, name, email)

            elif key == b"inward-sync":
                pass

except KeyboardInterrupt:
    pass

finally:
    consumer.close()
