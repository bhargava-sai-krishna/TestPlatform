#This file is used for running some functions and testing them individually or to generate something

from cryptography.fernet import Fernet
from sqlalchemy import create_engine, text
import secrets

from dotenv import load_dotenv
import os
load_dotenv()

def generate_fernet_key():
    print(Fernet.generate_key().decode()) 

def test_db_connection():
    engine = create_engine(os.getenv("DATABASE_URL"))
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users;"))  
        rows = result.fetchall()
        print("Database working. Rows fetched:", len(rows))

def generate_secret():
    print(secrets.token_hex(32))


# generate_fernet_key()
# test_db_connection()
generate_secret()