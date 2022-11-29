from .config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

settings = get_settings()

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

async def create_user(name: str,password: str):
    user = await users.insert_one({"name":name, "password":password })
    return user


    
    
