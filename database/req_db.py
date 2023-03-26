import motor.motor_asyncio
from info import REQ_SUB, REQ_DB

class JoinReqs:
    def __init__(self, url, c_name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self.client["JoinReqs"]
        self.col = self.db[str(c_name)]
      
    async def add_user(self, id):
        try:
            await self.col.insert_one({"_id": int(id),"user_id": int(id)})                                       
        except:
            pass

    async def get_user(self, id):
        return await self.col.find_one({"user_id": int(id)})

    async def get_all_users(self):
        return await self.col.find().to_list(None)

    async def delete_user(self, id):
        await self.col.delete_one({"user_id": int(id)})

    async def delete_all_users(self):
        await self.col.delete_many({})

    async def get_all_users_count(self):
        return await self.col.count_documents({})


db = JoinReqs(REQ_DB, REQ_SUB)

