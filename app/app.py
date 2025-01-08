import argparse
import time
from getpass import getpass
from typing import Any
import commands
import db


def welcome() -> tuple[Any, Any]:
    banner = r"""
# ===================================================================================== #
#                                                                                       #
#   /$$                           /$$             /$$                     /$$           #
#   | $$                          | $$            | $$                    | $$          #
#   | $$        /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$$ /$$   /$$  /$$$$$$$| $$   /$$    #
#   | $$       /$$__  $$ /$$_____/| $$  /$$/ /$$__  $$| $$  | $$ /$$_____/| $$  /$$/    #
#   | $$      | $$  \ $$| $$      | $$$$$$/ | $$  | $$| $$  | $$| $$      | $$$$$$/     #
#   | $$      | $$  | $$| $$      | $$_  $$ | $$  | $$| $$  | $$| $$      | $$_  $$     #
#   | $$$$$$$$|  $$$$$$/|  $$$$$$$| $$ \  $$|  $$$$$$$|  $$$$$$/|  $$$$$$$| $$ \  $$    #
#   |________/ \______/  \_______/|__/  \__/ \_______/ \______/  \_______/|__/  \__/    #
#                                                                                       #
# ===================================================================================== #

 🦆 Lockduck — Your Secure Terminal Password Manager 🦆
---------------------------------------------------------
     🛡️  Secured   |   🔒 Encrypted   |   ⚡ Fast
---------------------------------------------------------
Please choose an option to get started:
0: 🛑 Exit
1: 🔐 Login
2: 🆕 Create New Account
    """

    print(banner)
    action = None
    while action is None:
        try :
            action = int(input("Enter your choice (0-2): "))
            if action < 0 or action > 2:
                print("Invalid choice. Please enter a number between 0 and 2.")
                action = None
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 2.")
            action = None
    username, master_key = log_in(action)
    return username, master_key


def show_help():
    helper_text = """
======================================================
             🛠️  Lockduck Helper page  🛠️
======================================================

Usage: COMMAND [OPTIONS ARGUMENTS]

📋 Commands:

  🆕 create       Create a new record.
                 Usage: create -l <link> -u <username> -p <password>
                 Example: create -l website -u john -p johnpass

  📖 get          View existing records.
                 Usage: get [all | -l <link>]
                 Example: get all
                 Example: get -l website

  📝 update       Update an existing record.
                 Usage: update -l <link> -nl <new_link> -nu <new_username> -np <new_password>
                 Example: update -l website -nl newsite -nu newuser -np newpass

  🗑️ delete       Delete a record.
                 Usage: delete -l <link>
                 Example: delete -l website

  🎲 generate     Generate a random string.
                 Usage: generate [length]

⚙️ **Additional Commands**:

  ❓ help         Display this help message.
  🚪 exit | quit  Exit the application.
  🔒 logout       Log out of your current session
    """
    print(helper_text)


def log_in(action=None, counter=0) -> tuple[Any, Any]:
    match action:
        case 0:
            exit()
        case 1:
            if counter >= 3:
                wait_time = (counter - 2) * 2
                print(f"Too many failed attempts. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                welcome()
            username = input("Username: ").strip()
            password = getpass("Password: ").strip()
            is_logged_in = db.login(username, password)
            if not is_logged_in:
                print("Invalid username or password")
                return log_in(1, counter + 1)
            return username, password
        case 2:
            username = input("Username: ").strip()
            password = getpass("Password: ").strip()
            is_registered, error = db.register(username, password)
            if not is_registered:
                print(f"An error occurred during registration: {error}")
                return log_in()
            return username, password
        case _:
            print("Invalid action")


def parse_and_execute(user_id, master_key, command_input):
    parser = argparse.ArgumentParser(prog="Lockduck", description="Your secure password manager.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new record")
    create_parser.add_argument("-l", "--link", required=True, help="Link for the record")
    create_parser.add_argument("-u", "--username", required=True, help="Username for the record")
    create_parser.add_argument("-p", "--password", required=True, help="Password for the record")

    # Get command
    get_parser = subparsers.add_parser("get", help="Get records")
    get_parser.add_argument("-l", "--link", help="Link to fetch")
    get_parser.add_argument("-a", "--all", action="store_true", help="Get all records")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a record")
    update_parser.add_argument("-l", "--link", required=True, help="Link of the record to update")
    update_parser.add_argument("-nl", "--new-link", help="New link")
    update_parser.add_argument("-nu", "--new-username", help="New username")
    update_parser.add_argument("-np", "--new-password", help="New password")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a record")
    delete_parser.add_argument("-l", "--link", help="Link of the record to delete")
    delete_parser.add_argument("-a", "--all", action="store_true", help="Delete all records")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate a random password")
    generate_parser.add_argument("-l", "--length", type=int, default=12, help="Length of the password")

    try:
        args = parser.parse_args(command_input.split())
        match args.command:
            case "create":
                print(commands.create(user_id, master_key, vars(args)))
            case "get":
                if not (args.link or args.all):
                    print("Please provide a link or use --all to fetch all records.")
                    return
                if args.link and args.all:
                    print("Please provide either a link or use --all to fetch all records.")
                    return
                print(commands.read(user_id, master_key, vars(args)))
            case "update":
                if not (args.new_link or args.new_username or args.new_password):
                    print("Please provide at least one field to update.")
                    return
                print(commands.update(user_id, master_key, vars(args)))
            case "delete":
                if not (args.link or args.all):
                    print("Please provide a link or use --all to delete all records.")
                    return
                print(commands.delete(user_id, vars(args)))
            case "generate":
                print(commands.generate_password(args.length))
            case _:
                show_help()
    except SystemExit:
        print("Invalid input. Type 'help' for guidance.")


def app():
    db.init_db()
    username, master_key = welcome()
    while True:
        user_input = input(">> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        elif user_input.lower() == "logout":
            username, master_key = welcome()
        elif user_input.lower() == "help":
            show_help()
        else:
            user_id = commands.get_user_id(username)
            parse_and_execute(user_id, master_key, user_input)


if __name__ == "__main__":
    app()
