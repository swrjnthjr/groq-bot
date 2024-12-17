import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI


if load_dotenv("./.env"):
    print("ENV loaded!")
else:
    raise RuntimeError("Error while loading env")

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)

app = FastAPI()

companyName = "Swaraj and co."
custName = "Swastik Nath"

from app.routes import *
