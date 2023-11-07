from starlette.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI

from route.search_route import app as search_route

app = FastAPI()
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
    main()
