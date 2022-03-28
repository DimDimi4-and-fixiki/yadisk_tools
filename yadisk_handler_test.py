from yadisk_handler import YadiskHandler
from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv('YADISK_TOKEN')

yadisk_handler = YadiskHandler(token=token)
yadisk_handler.create_folder('/test_folder')

file_name = 'test_file.txt'
yadisk_handler.upload_file(local_path=file_name, remote_path=f'/test_folder/{file_name}')
print('Completed')