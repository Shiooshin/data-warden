from datetime import date
from common.storage.handler import StorageHandler
from typing import Dict
import json
import boto3
import config
from botocore.config import Config
from botocore.client import ClientError


class S3Handler(StorageHandler):
    __config__ = config.Config()

    __today_date__ = date.today().strftime("%Y-%m-%d")

    __bucket_name__ = __config__.get('bucket', 's3')
    __region_name__ = __config__.get('region', 's3')
    __s3__ = None

    __stats_file__ = f"{__today_date__}/stats"
    __repo_file__ = f"{__today_date__}/repos"

    def __init__(self) -> None:
        super().__init__()

        self.__s3__ = self.get_s3()

    def get_s3(self, configuration=None):

        if configuration is None:
            configuration = Config(region_name=self.__region_name__)

        return boto3.client('s3', config=configuration)

    def write_statistics_batch(self, data: Dict = dict()):
        self.write_batch(self.__stats_file__, data)

    def read_statistics_batch(self, keys: list = list()):
        return self.read_batch(self.__stats_file__)

    def read_repository_batch(self, keys: list = list()):
        return self.read_batch(self.__repo_file__)

    def write_repository_batch(self, data: Dict = dict()):
        self.write_batch(self.__repo_file__, data)

    def write_batch(self, filename, data: Dict = dict()):
        encoded = bytes(json.dumps(data).encode('UTF-8'))
        self.__s3__.put_object(Body=encoded,
                               Bucket=self.__bucket_name__,
                               Key=filename)

    def read_batch(self, filename):
        file = self.__s3__.get_object(Bucket=self.__bucket_name__,
                                      Key=filename)
        contents = file['Body'].read()
        return json.loads(contents.decode('UTF-8'))

    def connection_established(self):

        try:
            self.__s3__.meta.client.head_bucket(Bucket=self.__bucket_name__)
        except ClientError:
            print(f"No access to bucket or no permissions for {self.__bucket_name__}")
            return False

        return True
