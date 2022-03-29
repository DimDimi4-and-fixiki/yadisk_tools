from abstract_tools.abstract_yadisk_handler import AbstractYadiskHandler
from logging_tools.logger import Logger
from typing import AnyStr, List
import os
import traceback
import asyncio
from tqdm import tqdm


class YadiskHandler(AbstractYadiskHandler):
    def __init__(self, token: str, enable_logging=True):
        logger = Logger(module_name='yadisk_handler', log_file_path='yadisk_logs.log')
        self.enable_logging = enable_logging
        super().__init__(token, logger)

    def log(self, content: AnyStr, level='info'):
        if self.enable_logging:
            self.logger.log(msg=content, level=level)
        else:
            pass

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

    def create_download_task(self, local_path, remote_path):
        task_coroutine = self.disk_async.download(remote_path, local_path)
        task = asyncio.create_task(task_coroutine)
        self.tasks.append(task)

    def create_upload_task(self, local_path, remote_path):
        # task_coroutine =
        task = asyncio.create_task(self.disk_async.upload(path_or_file=local_path, dst_path=remote_path))
        self.tasks.append(task)

    def create_tasks(self, requests_params: List):
        """
        Creates asyncio tasks for making requests to YaDisk
        :param requests_params: List with parameters for the request,
                                Each element has:
                                - 'type' - type of the task (upload, download)
                                - 'local_path' - path to the local file
                                - 'remote_path' - path to the remote file on YaDisk
        """

        # Go through all requests params
        for requests_param in requests_params:

            # Get all params of the request
            request_type = requests_param['type']
            local_path = requests_param['local_path']
            remote_path = requests_param['remote_path']

            # Create upload request
            if request_type.lower() == 'upload':
                self.create_upload_task(local_path=local_path, remote_path=remote_path)

            # Create download task
            elif request_type.lower() == 'download':
                self.create_download_task(local_path=local_path, remote_path=remote_path)

            else:
                raise ValueError("Request type not in ('upload, download')")

    async def send_requests(self, request_params: List):
        """
        Coroutine for sending all async requests and awaiting all results
        """
        self.create_tasks(requests_params=request_params)

        # Join all asyncio tasks
        responses = await asyncio.gather(*self.tasks)
        await self.disk_async.close()

    def run_requests(self, request_params: List):

        # Then, we wait for all tasks to finish and collect results
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(self.send_requests(request_params=request_params))
        self.log(content='Execution of tasks completed', level='debug')
