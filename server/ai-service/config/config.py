import getpass
import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
model = ChatOpenAI(model="gpt-4.1")