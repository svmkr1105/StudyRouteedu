# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv

# load_dotenv()
# MONGO_URI = os.getenv("MONGODB_URI")

# try:
#     client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
#     db = client["studyroute"]
#     client.admin.command('ping')
#     print("✅ MongoDB Connected Successfully!")
# except Exception as e:
#     print(f"❌ MongoDB Connection Failed: {e}")
#     db = None



import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client["studyrouteeducation"]
    client.admin.command('ping')
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")
    db = None