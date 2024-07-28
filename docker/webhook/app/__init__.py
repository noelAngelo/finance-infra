import json
import os
from fastapi import FastAPI, Request
from loguru import logger

# Custom modules
from producer import send_message
from parser import ConfigParser

environment = os.environ.get("ENVIRONMENT")
config_path = os.environ.get("CONFIG_PATH")
config_root = os.environ.get("CONFIG_ROOT")

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):

    cp = ConfigParser(config_root=config_root, config_path=config_path, environment=environment)
    config = cp.config

    data = await request.body()
    logger.info(f"Received webhook data: {json.loads(data)}")
    send_message(broker=config.kafka.broker, topic=config.kafka.topic, value=data)
    logger.info("Message sent to Kafka")

    return {"statusCode": 201}
