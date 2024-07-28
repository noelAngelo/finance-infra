from confluent_kafka import Consumer, KafkaError, KafkaException
from loguru import logger


def consume_message(**conf):
    """Consume a message from a Kafka topic."""
    logger.debug(f"Consumer configuration: {conf}")
    c = Consumer(**conf)
    c.subscribe([conf['topic']])

    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.warning(f"End of partition reached {msg.topic()} [{msg.partition()}] offset {msg.offset()}")
                    continue
                else:
                    logger.error(f"Consumer error: {msg.error()}")
                    raise KafkaException(msg.error())

            logger.info(f"Message consumed: {msg.value(payload='').decode('utf-8')}")
    finally:
        c.close()
