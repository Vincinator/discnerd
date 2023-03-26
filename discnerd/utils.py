import configparser


def ask_parameter(value, name):
    if value is None:
        return input(f"{name} of disc?\n")
    else:
        return value

def load_config(path):
    config = configparser.ConfigParser()
    config.read_file(open(path))
    return config
