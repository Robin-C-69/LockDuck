import hashlib
import sqlite3

DB_PATH = "lockduck.db"

def init_db() :
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')
    con.commit()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(id)
    );
    """)

    con.commit()
    con.close()

def login(username = "", password = "") -> bool:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM Users WHERE name = ? AND password = ?", (username, hashed_password))
        user = cur.fetchone()
    except sqlite3.Error as error:
        print(f"An error occurred during login process : {error}")
        return False
    finally:
        con.close()

    return user is not None

def register(username="", password=""):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        # Check if user already exists
        cur.execute("SELECT * FROM Users WHERE name = ?", (username,))
        if cur.fetchone() is not None:
            return False, f"User {username} already exists"

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO Users (name, password) VALUES (?, ?)", (username, password_hash))
        con.commit()
    except sqlite3.Error as error:
        con.rollback()
        return False, error
    finally:
        con.close()
    return True, None
