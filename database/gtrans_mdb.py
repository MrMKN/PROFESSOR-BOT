import pymongo

from info import DATABASE_URI, DATABASE_NAME

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
mycol = mydb["USER"]

def insert(chat_id):
            user_id = int(chat_id)
            user_det = {"_id":user_id,"lg_code":None}
            try:
            	mycol.insert_one(user_det)
            except:
            	pass

def set(chat_id,lg_code):
	 mycol.update_one({"_id":chat_id},{"$set":{"lg_code":lg_code}})

	 	
def unset(chat_id):
	mycol.update_one({"_id":chat_id},{"$set":{"lg_code":None}})

def find(chat_id):
	id =  {"_id":chat_id}
	x = mycol.find(id)
	for i in x:
             lgcd = i["lg_code"]
             return lgcd 

def getid():
    values = []
    for key  in mycol.find():
         id = key["_id"]
         values.append((id)) 
    return values

def find_one(id):
	return mycol.find_one({"_id":id})
