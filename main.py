from sqlalchemy import sql
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from fastapi import FastAPI, Depends
import databases, sqlalchemy, uuid
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from fastapi import HTTPException
import os



SQLALCHEMY_DATABASE_URL = "postgresql://usertest:usertest222@127.0.0.1:5432/dbtest" #connect to postgresql 
# DATABASE_URL = "sqlite:///dbtest.db"
#SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = sqlalchemy.MetaData()

messages = sqlalchemy.Table(                ##creating The Table with id, message and counter to show views
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


class MessagesList(BaseModel):
    id: str
    message: str
    counter: int

class MessageEntry(BaseModel):
    message: str = Field(...,example = "hello world")

class MessageUpdate(BaseModel):
    id : str = Field(...,example = "Ente your id")
    message: str = Field(...,example = "hello world")


class MessageDelete(BaseModel):
    id: str = Field(..., example = "enter your id")


app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")           ##OAuth2 from FastApi
@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return {"access_token": form_data.username, "token_type": "bearer"}


async def return_message(Message: str):
    query = messages.select().where(messages.c.id == Message)        #returning message from table
    return await database.fetch_one(query)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/Messages", response_model=List[MessagesList])       ##returning all messages from the database
async def find_all_Messages():
    query=messages.select()

    return await database.fetch_all(query)


@app.post("/Create_message", response_model= MessagesList)           ##creating new message with id
async def register_message(mess: MessageEntry,token: str = Depends(oauth_scheme)):
    gID = str(uuid.uuid1())

    if(mess.message == ""):
        raise HTTPException(400,detail="bad Request")

    query = messages.insert(). values(
        id = gID,
        message = mess.message,
        counter = 0
    )
    await database.execute(query)
    return{
        "id": gID,
        **mess.dict(),
        "message": mess.message,
        "counter": 0
    }


@app.put("/Get_Message/{MessageID}", response_model = MessagesList)       ##returning existing message from the database. I used put to modify the counter.
async def find_message_by_id(MessageID: str):
    query = messages.update().\
        where(messages.c.id ==MessageID).\
            values(
                counter = messages.c.counter +1
            )
    await database.execute(query)

    return await return_message(MessageID)



@app.put("/Update_message", response_model = MessagesList)                   ##updating existing message from the database
async def update_message(Mess: MessageUpdate,token: str = Depends(oauth_scheme)):

    if(Mess.message == ""):
        raise HTTPException(400,detail="bad Request")

    query = messages.update().\
        where(messages.c.id ==Mess.id).\
            values(
                message = Mess.message,
                counter = 0
            )
    await database.execute(query)

    return await return_message(Mess.id)



@app.delete("/Message/{userID}")                                      ##deleting existing message
async def delete_message(Mess:MessageDelete,token: str = Depends(oauth_scheme)):
    query= messages.delete().where(messages.c.id == Mess.id)
    await database.execute(query)

    return "Deleted the message"
