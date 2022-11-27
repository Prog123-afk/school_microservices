from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import  CryptContext

from database import (
    get_users,
    update_user
)

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




