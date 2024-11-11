import click

import commands as command

def welcome():
    click.echo(click.style('Welcome to LockDuck', fg='green'))


def show_help():
    click.echo(click.style('Invalid command', fg='green'))


def app():
    welcome()
    while True:
        user_input = click.prompt(">>", prompt_suffix="" ,type=str)
        action = user_input.lower().split(" ")[0]
        args = user_input.lower().split(" ")[1:]

        if len(args) == 0 and action not in ["exit", "quit"]:
            show_help()
            continue


        match action:
            case "add":
                command.create(args)
            case "get":
                command.read(args)
            case "update":
                command.update(args)
            case "delete":
                command.delete(args)
            case "exit" | "quit":
                break
            case _:
                show_help()


if __name__ == "__main__" :
    app()
