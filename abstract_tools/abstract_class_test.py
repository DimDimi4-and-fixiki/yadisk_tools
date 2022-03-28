import os

from abstract_yadisk_handler import AbstractYadiskHandler
from dotenv import load_dotenv
from yadisk import YaDisk

load_dotenv()


token = os.getenv('YADISK_TOKEN')
yadisk = YaDisk(token=token)
print(yadisk)