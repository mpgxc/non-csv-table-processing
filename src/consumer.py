import os
import json
import boto3
import logging
from typing import Any, Dict, List

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

QUEUE_URL = os.getenv("QUEUE_URL")
SQS = boto3.client("sqs")


from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def consumer(event: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Função para consumir mensagens da fila do SQS.
    """

    for record in event["Records"]:
        try:
            logger.info(f'Message body: {record["body"]}')
            logger.info(
                f'Message attribute: {record["messageAttributes"]["AttributeName"]["stringValue"]}'
            )
        except KeyError as e:
            logger.error(f"Error processing record: {e}")

    return {"statusCode": 200, "body": json.dumps({"message": "Messages processed"})}
