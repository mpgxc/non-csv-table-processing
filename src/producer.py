import os
import json
import boto3
import logging
from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

QUEUE_URL = os.getenv("QUEUE_URL")
SQS = boto3.client("sqs")


def producer(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função para enviar mensagens para a fila do SQS.
    """

    if not event.get("body"):
        return {"statusCode": 400, "body": json.dumps({"message": "No body was found"})}

    try:
        message_attrs = {
            "AttributeName": {"StringValue": "AttributeValue", "DataType": "String"}
        }

        SQS.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=event["body"],
            MessageAttributes=message_attrs,
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"messages": "Message accepted!"}),
        }

    except Exception as e:
        logger.exception("Sending message to SQS queue failed!")

        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}
