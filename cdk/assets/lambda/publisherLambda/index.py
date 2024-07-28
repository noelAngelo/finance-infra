import boto3
from loguru import logger


def handler(event, context):
    logger.info(f"Received event: {event}")
    
    body = event.get("body")

    return {
        "statusCode": 200,
        "body": f"Hello from Publisher Lambda! - {body}"
    }