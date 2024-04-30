import requests
import logging
import boto3
from typing import Any, Literal, TypedDict
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class BucketParams(TypedDict):
    Bucket: str
    Key: str


type ClientMethod = Literal["get", "put_object"]


def create_s3_client() -> Any:
    """Cria e retorna um cliente S3."""

    return boto3.client("s3")


def generate_presigned_url(
    s3_client: Any,
    client_method: ClientMethod,
    method_parameters: BucketParams,
    expires_in: int,
) -> str:
    """
    Gera uma URL pré-assinada para operações no S3.
    """

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
        )

        logger.info("URL pré-assinada obtida: %s", url)

        return url
    except ClientError as error:
        logger.exception(
            "Não foi possível obter a URL pré-assinada para o método '%s'.",
            client_method,
            error,
        )

        raise


def upload_file_to_s3(url: str, file_path: str) -> None:
    """
    Faz o upload de um arquivo para o S3 usando uma URL pré-assinada.
    """

    with open(file_path, mode="rb") as file:
        http_response = requests.put(url, data=file)

        if http_response.status_code in range(200, 300):
            logger.info("Arquivo carregado com sucesso.")
        else:
            logger.error(
                "Falha ao carregar arquivo no S3. Código de status: %s",
                http_response.status_code,
            )


def main():
    try:
        s3_client = create_s3_client()
        file_name = "file.xlsx"

        url = generate_presigned_url(
            s3_client=s3_client,
            client_method="put_object",
            method_parameters={"Bucket": "non-csv-processing", "Key": file_name},
            expires_in=3600,
        )

        upload_file_to_s3(url, f"src/{file_name}")

    except Exception as e:
        logger.error("Erro: %s", e)
        raise


if __name__ == "__main__":
    main()
