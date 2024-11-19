import pymongo
import logging

from backend.config import settings


logging.getLogger('pymongo').setLevel(logging.ERROR)
logging.getLogger('matplotlib').setLevel(logging.ERROR)

DATABASE_URL = settings.database_url
DATABASE_NAME = settings.database_name

client = pymongo.MongoClient(DATABASE_URL)


database = client[DATABASE_NAME]
