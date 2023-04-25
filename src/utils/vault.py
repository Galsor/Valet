import os


def get_openai_secret():
    return os.getenv("OPENAI_API_KEY")
