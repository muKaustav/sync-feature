from decouple import config
from confluent_kafka import Producer

producer_config = {
    "bootstrap.servers": f'{config("HOST_IP")}:9092',
    "client.id": "zenskar-producer",
}

kafka_producer = Producer(producer_config)


def produce_message(topic, key, value):
    kafka_producer.produce(topic, key=key, value=value)
    kafka_producer.flush()
