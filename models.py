from pydantic import BaseModel, Field

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