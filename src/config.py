import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))

def get_url(sync=False):
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    # Используем asyncpg для асинхронности
    if sync: 
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

def get_secret_key():
    return os.getenv("JWT_SECRET_KEY")