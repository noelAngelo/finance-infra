from confluent_kafka import Producer
from loguru import logger


def delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def send_message(broker: str, **kwargs):
    """Send a message to a Kafka topic."""
    producer_conf = {"bootstrap.servers": broker}
    logger.debug(f"Producer configuration: {producer_conf}")
    p = Producer(producer_conf)
    p.produce(callback=delivery_report, **kwargs)
    p.flush()
