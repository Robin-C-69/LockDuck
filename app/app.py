import click
import commands as command
from db_models import init_db


def welcome():
    click.echo(click.style('Welcome to LockDuck', fg='green'))


def show_help():
    click.echo(click.style('get some help here', fg='green'))


def app():
    welcome()
    init_db()
    master_key="master_key" #TODO
    while True:
        user_input = click.prompt(">>", prompt_suffix="" ,type=str)
        action = user_input.lower().split(" ")[0]
        args = user_input.lower().split(" ")[1:]

        if len(args) == 0 and action not in ["exit", "quit"]:
            show_help()
            continue

        match action:
            case "add":
                transaction_result = command.create(master_key, args)
                click.echo(transaction_result)
            case "get":
                transaction_result = command.read(master_key, args)
                click.echo(transaction_result)
            case "update":
                transaction_result = command.update(master_key, args)
                click.echo(transaction_result)
            case "delete":
                transaction_result = command.delete(args)
                click.echo(transaction_result)
            case "exit" | "quit":
                break
            case _:
                show_help()


if __name__ == "__main__" :
    app()
