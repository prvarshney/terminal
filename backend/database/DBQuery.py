# This module acts as an API for CRUD operations in database
from pymongo import MongoClient
import config

# Creating connection with the mongodb database
client = MongoClient(config.MongoDB_URI)