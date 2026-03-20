import os
from dotenv import load_dotenv

load_dotenv()

def get_secret(key:str):

    # Check for _FILE suffix first
    file_env = f"{key}_FILE"

    if file_env in os.environ:
        with open(os.environ[file_env], 'r') as f:
            return f.read().strip()


DB_PASSWORD = get_secret('DB_PASSWORD')
DB_USER = os.getenv('DB_USER', 'vigilia')
DEFAULT_DATABASE = os.getenv('DATABASE_NAME', 'vigilia')
DB_IP_AND_PORT = os.getenv('DB_IP_AND_PORT', 'vigilia-db:5432')
DATABASE_URL =  f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_IP_AND_PORT}/{DEFAULT_DATABASE}'
