from sqlalchemy import sql
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from fastapi import FastAPI, Depends
import databases, sqlalchemy, uuid
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
import os



SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# DATABASE_URL = "sqlite:///dbtest.db"

database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = sqlalchemy.MetaData()

messages = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("message", sqlalchemy.String),
    sqlalchemy.Column("counter", sqlalchemy.Integer),

)

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL
)
metadata.create_all(engine)


class UserList(BaseModel):
    id: str
    message: str
    counter: int

class UserEntry(BaseModel):
    message: str = Field(...,example = "hello world")

class UserUpdate(BaseModel):
    id : str = Field(...,example = "Ente your id")
    message: str = Field(...,example = "hello world")

class GetUser(BaseModel):
    id : str = Field(...,example = "Ente your id")
    message: str = Field(...,example = "hello world")
    counter: int
class UserDelete(BaseModel):
    id: str = Field(..., example = "enter your id")


app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return {"access_token": form_data.username, "token_type": "bearer"}


async def return_user(userId: str):
    query = messages.select().where(messages.c.id == userId)
    return await database.fetch_one(query)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users", response_model=List[UserList])
async def find_all_users():
    query=messages.select()

    return await database.fetch_all(query)

@app.post("/users", response_model= UserList)
async def register_user(user: UserEntry,token: str = Depends(oauth_scheme)):
    gID = str(uuid.uuid1())
    query = messages.insert(). values(
        id = gID,
        message = user.message,
        counter = 0
    )
    await database.execute(query)
    return{
        "id": gID,
        **user.dict(),
        "message": user.message,
        "counter": 0
    }

@app.put("/users/{userID}", response_model = UserList)
async def find_user_by_id(userID: str):
    query = messages.update().\
        where(messages.c.id ==userID).\
            values(
                counter = messages.c.counter +1
            )
    await database.execute(query)

    return await return_user(userID)



@app.put("/users", response_model = UserList)
async def update_user(user: UserUpdate,token: str = Depends(oauth_scheme)):
    query = messages.update().\
        where(messages.c.id ==user.id).\
            values(
                message = user.message,
                counter = 0
            )
    await database.execute(query)

    return await return_user(user.id)

@app.delete("/users/{userID}")
async def delete_user(user:UserDelete,token: str = Depends(oauth_scheme)):
    query= messages.delete().where(messages.c.id == user.id)
    await database.execute(query)

    return "Deleted the message"
