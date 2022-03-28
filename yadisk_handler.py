from abstract_tools.abstract_yadisk_handler import AbstractYadiskHandler
import logging
from logging_tools.logger import Logger
from typing import AnyStr, List
import os
import traceback
import aiohttp
import asyncio


class YadiskHandler(AbstractYadiskHandler):
    def __init__(self, token: str):
        logger = Logger(module_name='yadisk_handler', log_file_path='yadisk_logs.log')
        super().__init__(token, logger)

    def log(self, content: AnyStr, level='debug'):
        self.logger.log(msg=content, level=level)

    def create_folder(self, directory_path: AnyStr):
        self.disk.mkdir(path=directory_path)

    def upload_file(self, local_path, remote_path):
        dir_path, file_name = os.path.split(local_path)
        try:
            self.disk.upload(path_or_file=local_path, dst_path=remote_path)
            self.log(f'File {file_name} uploaded to YaDisk', level='info')

        except Exception as e:
            traceback.print_exc()

    def download_file(self, local_path, remote_path):
        dir_path, file_name = os.path.split(remote_path)
        try:
            self.disk.download(remote_path, local_path)
            self.log(f'File {file_name} downloaded from YaDisk', level='info')

        except Exception as e:
            traceback.print_exc()

    def create_download_task(self, session: aiohttp.ClientSession, local_path, remote_path):
        pass

    def create_upload_task(self, session: aiohttp.ClientSession, local_path, remote_path):
        pass

    def create_tasks(self, requests_params: List):
        pass

    async def send_requests(self):
        """
        Coroutine for sending all async requests and awaiting all results
        """
        pass

    def run_requests(self, request_params: List):
        # Firstly, we create all async tasks
        self.create_tasks(requests_params=request_params)

        # Then, we wait for all tasks to finish and collect results
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(self.send_requests())
        return self.responses
