from yadisk_handler import YadiskHandler
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()
token = os.getenv('YADISK_TOKEN')

yadisk_handler = YadiskHandler(token=token, enable_logging=True)

remote_folder = '/test_folder'
local_folder = r'C:\Users\DimDimi4\Documents\yandex_disk_loader\yadisk_tools\Xml_files'

requests_params = []
for file in tqdm(os.listdir(local_folder)[3500:3700]):
    local_path = os.path.join(local_folder, file)
    remote_path = f'/test_folder/{file}'
    request_param = {
        'type': 'upload',
        'local_path': local_path,
        'remote_path': remote_path
    }
    requests_params.append(request_param)


yadisk_handler.run_requests(requests_params)

print(yadisk_handler.responses)
# for file in tqdm(os.listdir(local_folder)[200:300]):
#     file_path = os.path.join(local_folder, file)
#     yadisk_handler.upload_file(local_path=file_path, remote_path=f'/test_folder/{file}')

