from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import  CryptContext

from .database import (
    get_users,
    update_user,
#    create_user,
)
#from .schema import User

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/api/hash_all")
async def hash_users():
    users = await get_users()
    errs = []
    for user in users:
        hash = pwd_ctx.hash(user["password"])
        done = await update_user(user["id"], {"password_hash":hash})
        if not done:
            errs.append(f"Failed to hash password of {user.name}")

    if errs:
        return {
            "msg":"some user's password could not be hashed",
            "err": errs
        }
    return { "msg": "Task done!" }



"""
@app.post("/user/create")
async def user_add(user: User):
    u = await create_user(user.name, user.password)
    print(u)
    return {}

@app.get("/user")
async def get_users_list():
    users = await get_users()
    users = list(map(rem_id, users))
    return {"users":users}


def rem_id(x):
    del x["id"]
    return x
"""
