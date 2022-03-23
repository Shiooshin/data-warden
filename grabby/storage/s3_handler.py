from datetime import date
from handler import StorageHandler
from typing import Dict
import json
import boto3
from botocore.config import Config


class S3Handler(StorageHandler):
    __bucket_name__ = "data-warden-statistics"
    __s3__ = None

    def __init__(self) -> None:
        super().__init__()

        self.__s3__ = self.get_s3()

    def get_s3(self, configuration=None):

        if configuration is None:
            configuration = Config(region_name='us-west-2')

        return boto3.client('s3', config=configuration)

    def write_statistics_batch(self, data: Dict = dict()):
        encoded = bytes(json.dumps(data).encode('UTF-8'))
        self.__s3__.put_object(Body=encoded,
                               Bucket=self.__bucket_name__,
                               Key=self.compose_date())

    def read_statistics_batch(self, keys: list = list()):
        file = self.__s3__.get_object(Bucket=self.__bucket_name__,
                                      Key=self.compose_date())
        contents = file['Body'].read()
        return json.loads(contents.decode('UTF-8'))

    def compose_date():
        return date.today().strftime("%Y-%m-%d")

    def read_repository_batch(self, keys: list = list()):
        pass

    def write_repository_batch(self, data: Dict = dict()):
        pass
