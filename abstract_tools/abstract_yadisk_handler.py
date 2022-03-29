import logging
from abc import ABC, abstractmethod
from yadisk import YaDisk
from typing import AnyStr, List
import aiohttp
import asyncio
from yadisk_async import YaDisk as YaDiskAsync


class AbstractYadiskHandler(ABC):
    def __init__(self, token: str, logger=None):

        # Initialize token for YaDisk
        self.token = token

        # Create sync and async versions of YaDisk object based on token
        self.disk = YaDisk(token=self.token)
        self.disk_async = YaDiskAsync(token=self.token)

        # Set logger for YaDisk Handler object
        if logger is not None:
            self.logger = logger

        # List for asyncio tasks and API responses
        self.tasks, self.responses = [], []

        self._check_token()

    def _check_token(self):
        """
        Method for validating Yandex.Disk token
        :returns:
            - True if token is valid
            - Raises Error and returns False if token is not valid
        """

        # Use yadisk method to check if token is valid
        if self.disk.check_token():
            self.log('YaDisk token is valid')
            return True

        # Raise an Exception if token is not valid
        else:
            self.log('YaDisk token is not valid')
            raise ValueError('YaDisk Token Error occurred, check your YaDisk token')

        return False

    @abstractmethod
    def log(self, content: AnyStr, level='debug'):
        pass

    @abstractmethod
    def upload_file(self, local_path, remote_path):
        """
        Abstract method for uploading file to the Yandex Disk storage
        :param local_path: local path to file
        :param remote_path: path to file on Yandex.Disk
        """
        pass

    @abstractmethod
    def download_file(self, local_path, remote_path):
        """
        Abstract method for downloading file from Yandex Disk storage
        :param local_path: local path to file
        :param remote_path: path to file on Yandex.Disk
        """
        pass

    @abstractmethod
    def create_upload_task(self, local_path, remote_path):
        """
        Abstract method for creating async upload task
        :param session: aiohttp session for making request
        :param local_path: local path to file
        :param remote_path: path to file on Yandex.Disk
        """
        pass

    @abstractmethod
    def create_download_task(self, local_path, remote_path):
        """
        Abstract method for creating async download task
        :param session: aiohttp session for making request
        :param local_path: local path to file
        :param remote_path: path to file on Yandex.Disk
        """
        pass

    @abstractmethod
    def create_tasks(self, requests_params: List):
        pass

    @abstractmethod
    async def send_requests(self):
        """
        Coroutine for sending all async requests and awaiting all results
        """
        pass

    @abstractmethod
    def run_requests(self, request_params: List):
        """
        Abstract method for sending async requests and
        :param request_params: list with requests params
        """
        pass


