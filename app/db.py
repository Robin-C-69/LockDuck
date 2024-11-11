"""
DB connection

CRUD
- SQL requests
"""
import sqlite3

# Define global variables
DB_NAME = "lockduck.db"

def connect_to_db(db_name: str):
    return sqlite3.connect(db_name)

def create(credentials: dict):
    return f"create: {credentials}"

def read(credentials: dict):
    return f"get: {credentials}"

def update(credentials: dict):
    return f"update: {credentials}"

def delete(credentials: dict):
    return f"delete: {credentials}"
