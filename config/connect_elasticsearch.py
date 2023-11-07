import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the values from environment variables
es_host = os.getenv("ELASTICSEARCH_URL")
es_username = os.getenv("ELASTICSEARCH_USER")
es_password = os.getenv("ELASTICSEARCH_PASSWORD")

# Connect to Elasticsearch with environment variables
es = Elasticsearch([es_host], http_auth=(es_username, es_password))