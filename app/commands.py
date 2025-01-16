import sqlite3
import texttable
from db import DB_PATH
from encryption import password_encrypt, password_decrypt
import random
import string

ITERATIONS = 100_000


def format_in_table(rows_list) -> str:
    table_obj = texttable.Texttable()
    table_obj.set_cols_align(['l', 'l', 'l'])
    table_obj.set_cols_dtype(['t', 't', 't'])
    table_obj.set_cols_valign(['m', 'm', 'm'])
    table_obj.add_rows([["Link", "Username", "Password"]] + rows_list)
    return table_obj.draw()


def get_user_id(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id FROM Users WHERE name = ?", (username,))
    user_id = cur.fetchone()[0]
    con.close()
    return user_id


def create(user_id: int, master_key: str, args) -> str:
    password = args["password"]
    link = args["link"]
    username = args["username"]
    encrypted_password = password_encrypt(password.encode(), master_key, ITERATIONS).decode()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("SELECT username FROM Credentials WHERE link = ?", (link,))
        if cur.fetchone() is not None:
            return f"Link {link} already exists"
        cur.execute(
            "INSERT INTO Credentials (link, username, password, user_id) VALUES (?, ?, ?, ?)",
            (link, username, encrypted_password, user_id),
        )
        con.commit()
        return f"New credential created for {username} with link {link}"
    except sqlite3.Error as error:
        con.rollback()
        return str(error)
    finally:
        con.close()


def read(user_id: int, master_key: str, args) -> str:
    link = args.get("link", False)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        command = "SELECT link, username, password FROM Credentials WHERE user_id = ?"
        if link:
            command += " AND link = ?"
        cur.execute(
            command,
            (user_id, link) if link else (user_id,),
        )
        rows = cur.fetchall()
        if not rows:
            return "No credentials found" + (f" for {link}" if link else "")
        res = []
        for r in rows:
            row = list(r)
            decrypted_password = password_decrypt(row[2], master_key).decode()
            row[2] = decrypted_password
            res.append(row)
        rows_table_formatted = format_in_table(res)
        return rows_table_formatted
    except sqlite3.Error as error:
        return str(error)
    finally:
        con.close()


def update(user_id: int, master_key, args) -> str:
    link = args.get("link", False)
    new_link = args.get("new_link", None)
    new_username = args.get("new_username", None)
    new_password = args.get("new_password", None)

    if not (new_link or new_username or new_password):
        return "Nothing to update."

    new_link = new_link or link

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        if not new_username or not new_password:
            cur.execute(
                "SELECT username, password FROM Credentials WHERE link = ? AND user_id= ?",
                (link, user_id),
            )
            result = cur.fetchone()
            if result:
                new_username = new_username or result[0]
                new_password = new_password or password_decrypt(result[1], master_key).decode()
            else:
                return f"No credentials found for {link}"

        encrypted_password = password_encrypt(new_password.encode(), master_key, ITERATIONS).decode()
        cur.execute(
            "UPDATE Credentials SET link = ?, username = ?, password = ? WHERE link = ? AND user_id = ?",
            (new_link, new_username, encrypted_password, link, user_id),
        )
        con.commit()
        return f"Updated credentials for {new_username} with link {new_link}"
    except sqlite3.Error as error:
        con.rollback()
        return str(error)
    finally:
        con.close()


def delete(user_id: int, args) -> str:
    link = args.get("link", False)
    if link :
        confirmation = input(f"Are you sure you want to delete the credentials for {link} ? (y/n): ").strip().lower()
    else:
        confirmation = input("Are you sure you want to delete all credentials ? (y/n): ").strip().lower()
    if confirmation not in ["y", "yes"]:
        return "Deletion cancelled"
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        command = "DELETE FROM Credentials WHERE user_id = ?"
        if link:
            command += " AND link = ?"
        cur.execute(command, (user_id, link) if link else (user_id,))
        con.commit()
        if link:
            res = f"Successfully deleted credentials for {link}" if cur.rowcount else f"No credentials found for {link}"
        else:
            res = f"Successfully deleted all credentials" if cur.rowcount else f"No credentials found"
        return res
    except sqlite3.Error as error:
        con.rollback()
        return str(error)
    finally:
        con.close()


def generate_password(length=12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
