import sqlite3
import texttable
from app import show_help
from db import DB_PATH
from encryption import password_encrypt, password_decrypt
import random
import string

ITERATIONS = 100_000


def args_to_dict(params, flag_map, autocomplete=False):
    res = {key: "" for key in flag_map.values()}
    # res = {}
    i = 0

    while i < len(params):
        flag = params[i]
        if flag in flag_map:
            next_param = params[i + 1] if i + 1 < len(params) else None
            if next_param and next_param not in flag_map:
                res[flag_map[flag]] = next_param
                i += 2
            else:
                if autocomplete:
                    res[flag_map[flag]] = ""
                i += 1
        else:
            return None

    return res


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


def create(user_id: int, master_key: str, *args) -> str:
    def parse_command(command):
        params = command[0]
        flag_map = {
            "-l": "link",
            "-u": "username",
            "-p": "password",
        }
        command_dict = args_to_dict(params, flag_map)
        return command_dict

    parsed = parse_command(args)
    if parsed is None:
        show_help()
        return ""

    password = parsed['password']
    link = parsed['link']
    username = parsed['username']
    encrypted_password = password_encrypt(password.encode(), master_key, ITERATIONS).decode()

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("SELECT username from Credentials where link = ?", (link,))
        if cur.fetchone() is not None:
            return f"link {link} already exists"
        cur.execute("INSERT INTO Credentials (link, username, password, user_id) VALUES (?, ?, ?, ?)",
                    (link, username, encrypted_password, user_id))
        con.commit()
        return f"New credential created for {username} with link {link}"
    except sqlite3.Error as error:
        con.rollback()
        return str(error)
    finally:
        con.close()


def read(user_id: int, master_key: str, *args) -> str:
    def parse_command(command):
        params = command[0]
        flag_map = {
            "-l": "link",
        }
        command_dict = args_to_dict(params, flag_map)
        return command_dict

    parsed = parse_command(args)

    if parsed is None:
        show_help()
        return ""

    link = parsed['link']
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("SELECT link, username, password FROM Credentials WHERE link = ? AND user_id = ?", (link, user_id))
        rows = cur.fetchall()
        if len(rows) == 0 :
            return f"No credentials found for {link}"
        res = []
        for r in rows:
            row = list(r)
            decrypted_password = password_decrypt(row[2], master_key).decode()
            row[2] = decrypted_password
            res.append(row)
        rows_list = [row for row in res]
        rows_table_formated = format_in_table(rows_list)
        return rows_table_formated
    except sqlite3.Error as error:
        return str(error)
    finally:
        con.close()


def update(user_id: int, master_key, *args) -> str:
    def parse_command(command):
        params = command[0]
        flag_map = {
            "-l": "link",
            "-nl": "new_link",
            "-nu": "username",
            "-np": "password",
        }
        command_dict = args_to_dict(params, flag_map, autocomplete=True)
        return command_dict

    parsed = parse_command(args)
    if parsed is None:
        show_help()
        return ""

    link = parsed['link']

    if link == "":
        return f"You need to specify a link to update your credentials\nProvided link: {link}"

    if parsed['new_link'] == "" and parsed['username'] == "" and parsed['password'] == "":
        return f"Nothing to update"

    new_link = parsed['new_link'] if parsed['new_link'] != "" else link

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Retrieve missing credentials
    if not parsed['username'] or not parsed['password']:
        try:
            cur.execute("SELECT username, password FROM Credentials WHERE link = ? AND user_id= ?", (link, user_id))
            result = cur.fetchone()
            if result:
                parsed['username'] = parsed['username'] or result[0]
                parsed['password'] = parsed['password'] or password_decrypt(result[1], master_key).decode()
            else:
                return f"No credentials found for {link}\nUpdate canceled"
        except sqlite3.Error as error:
            con.rollback()
            return str(error)

    # Update
    try:
        encrypted_password = password_encrypt(parsed['password'].encode(), master_key, ITERATIONS).decode()
        if "-np" in args[0]:
            cur.execute("UPDATE Credentials SET link = ?, username = ?, password = ? WHERE link = ? AND user_id = ?",
                    (new_link, parsed['username'], encrypted_password, link, user_id))
        else :
            cur.execute("UPDATE Credentials SET link = ?, username = ? WHERE link = ? AND user_id = ?",
            (new_link, parsed['username'], link, user_id))
        con.commit()
        return f"Updated credentials for {parsed['username']} with link {new_link}"
    except sqlite3.Error as error:
        con.rollback()
        return str(error)
    finally:
        con.close()


def delete(user_id: int, *args) -> str:
    def parse_command(command):
        params = command[0]
        flag_map = {
            "-l": "link",
        }
        command_dict = args_to_dict(params, flag_map)
        return command_dict

    parsed = parse_command(args)
    if parsed is None:
        show_help()
        return ""

    link = parsed['link']

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute("DELETE FROM Credentials WHERE link = ? AND user_id = ?", (link, user_id))
        con.commit()
        if cur.rowcount == 0:
            return f"No credentials found for {link}"
        else :
            return f"Successfully deleted credentials for {link}"
    except sqlite3.Error as error:
        con.rollback()
        return str(error)
    finally:
        con.close()

def generate_password(length=12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password