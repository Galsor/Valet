import os


def get_openai_secret():
    return os.getenv("OPENAI_API_KEY")


def get_pinecone_secret():
    return os.getenv("PINECONE_API_KEY")

