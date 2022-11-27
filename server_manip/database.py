from core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.coders
users = db.get_collection("users")

def user_helper(user) -> dict:
    return {
        "id": user["_id"],
        "name": user["name"],
        "password": user["password"],
    }

async def get_users():
    u = []
    async for user in users.find():
        u.append(user_helper(user))
    return u

async def update_user(id: str,data: dict):
    user = await users.find_one({"_id": ObjectId(id)})
    if user:
        updated = await users.update_one(
            {"_id":ObjectId(id)},
            {"$set":data}
        )
        if updated:
            return True
    return False


    
    
