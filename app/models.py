from pydantic import BaseModel


class ChatInput(BaseModel):
    user_input: str


class ChatOutput(BaseModel):
    success: bool
    message: str
