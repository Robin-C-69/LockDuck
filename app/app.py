import time
from typing import Any
import click
import commands as command
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

    click.echo(banner)
    action = click.prompt("Enter your choice (0-2):", prompt_suffix="", type=int)
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
                 Example: read all
                 Example: read -l website

  📝 update       Update an existing record.
                 Usage: update -l <link> -nl <new_link> -nu <new_username> -np <new_password>
                 Example: update -l website -nl website -nu newjohn -np newjohnpassword

  🗑️ delete       Delete a record.
                 Usage: delete -l <link>
                 Example: delete -l website

  🎲️ generate     Generate a random string.
                 Usage: generate [length]

⚙️ **Additional Commands**:

  ❓ help         Display this help message.
  🚪 exit | quit  Exit the application.
  🔒 logout       Log out of your current session

    """
    click.echo(helper_text)


def log_in(action=None, counter = 0) -> tuple[Any, Any]:
    match action:
        case 0:
            exit()
        case 1:
            if counter >= 3 :
                wait_time = (counter - 2) * 2  # Starting at 2 seconds for the 3rd failed attempt, 4 for the 4th, etc.
                click.echo(f"Too many failed attempts. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                welcome()
            username = click.prompt('Username', prompt_suffix=":", type=str)
            password = click.prompt('Password', prompt_suffix=":", type=str, hide_input=True)
            is_logged_in = db.login(username, password)
            if not is_logged_in:
                click.echo(click.style('Invalid username or password', fg='red'))
                log_in(1, counter+1)
            return username, password
        case 2:
            username = click.prompt('Username', prompt_suffix=":", type=str)
            password = click.prompt('Password', prompt_suffix=":", type=str, hide_input=True)
            is_registered, error = db.register(username, password)
            if not is_registered:
                click.echo(click.style(f'An error occurred during registration: {error}', fg='red'))
                log_in()
            return username, password
        case _:
            click.echo(click.style('Invalid action', fg='red'))


def app():
    db.init_db()
    username, master_key = welcome()
    while True:
        user_input = click.prompt(">>", prompt_suffix="", type=str)
        action = user_input.lower().split(" ")[0]
        args = user_input.lower().split(" ")[1:]

        if len(args) == 0 and action not in ["exit", "quit", "logout", "generate", "help"]:
            show_help()
            continue

        user_id = command.get_user_id(username)

        match action:
            case "create":
                transaction_result = command.create(user_id, master_key, args)
                click.echo(transaction_result)
            case "get":
                transaction_result = command.read(user_id, master_key, args)
                click.echo(transaction_result)
            case "update":
                transaction_result = command.update(user_id, master_key, args)
                click.echo(transaction_result)
            case "delete":
                transaction_result = command.delete(user_id, args)
                click.echo(transaction_result)
            case "exit" | "quit":
                break
            case "logout":
                username, master_key = welcome()
            case "generate":
                length = args[0] if args else 12
                click.echo(command.generate_password(int(length)))
            case _:
                show_help()


if __name__ == "__main__":
    app()
