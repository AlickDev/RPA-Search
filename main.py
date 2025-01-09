from starlette.middleware.cors import CORSMiddleware
from watchgod import run_process
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
import os

from route.search_route import app as search_route

app = FastAPI(
    title="RPA",
    version="1.0.2",
    # servers=[
    #     {
    #         "url": "http://172.16.203.30:8000",
    #         "description": "Local development server"
    #     },
    #     {
    #         "url": "http://0.0.0.0:8000",
    #         "description": "Local development server"
    #     },
    # ],
    terms_of_service="https://github.com/Somchan/RPA-Serach.git",
)

origins = ["*"]
app.include_router(search_route)

# Load environment variables from .env file
load_dotenv()

PORT = os.getenv("PORT")
HOST_URL = os.getenv("HOST_URL")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def main():
    uvicorn.run(app, host=HOST_URL, port=int(PORT))


if __name__ == '__main__':
    run_process('.', main)

# Run
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
# .venv\Scripts\activate

# uvicorn main:app --reload
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
