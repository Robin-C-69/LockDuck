from app import show_help
import db as db


def args_to_dict(params, flag_map):
    res = {}
    try:
        i = 0
        while i < len(params):
            if params[i] in flag_map and params[i + 1] not in flag_map:
                res[flag_map[params[i]]] = params[i + 1]
                i += 2
            else:
                res = None
                break
    except IndexError:
        return None
    return res


def create(*args):
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
        return

    #TODO
    sql_res = db.create(parsed)
    print(sql_res)


def read(*args):
    def parse_command(command):
        params = command[0]
        flag_map = {
            "-l": "link",
            "-u": "username",
        }
        command_dict = args_to_dict(params, flag_map)
        return command_dict

    parsed = parse_command(args)

    if parsed is None:
        show_help()
        return

    #TODO
    sql_res = db.read(parsed)
    print(sql_res)


def update(*args):
    def parse_command(command): #TODO : Check what params will be there
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
        return

    #TODO
    sql_res = db.update(parsed)
    print(sql_res)


def delete(*args):
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
        return

    #TODO
    sql_res = db.delete(parsed)
    print(sql_res)