#!/bin/python3
import click
import yaml
import pickle
import configparser
import os
import pprint
from pathlib import Path
from os.path import expanduser

DEFAULT_CONFIG_PATH = "~/.config/discnerd"
DEFAULT_CONFIG_NAME = "config"

class Context(object):
    config: configparser.ConfigParser
    
    def __init__(self, config=None):
        if config is None:
            self.config = config
def default_config():
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'DataPath': '~/.config/discnerd/data.yml'
    }

    return config

    
def load_config(path):
    config = configparser.ConfigParser()
    config.read_file(open(path))
    return config


@click.group()
@click.option('--config', type=str)
@click.pass_context
def cli(ctx, config):
    ctx.obj = {}
    # User provided config path
    if config is not None:
        config = expanduser(config)
        if os.path.isfile(config):
            cfg = load_config(config)
            ctx.obj['config'] = cfg
            print(f"INFO: {config} config loaded")
        else:    
            print(f"ERROR: {config} is not a file")
            return
    # Use Default config path
    else:
        config = expanduser(f"{DEFAULT_CONFIG_PATH}/{DEFAULT_CONFIG_NAME}")
        Path(expanduser(DEFAULT_CONFIG_PATH)).mkdir(parents=True, exist_ok=True)    
        # default config path exists, use it
        if os.path.isfile(config):
            cfg = load_config(config)
            ctx.obj['config'] = cfg
            print(f"INFO: {config} config loaded")
        # Default config path does not exist, create it
        else:
            print(f"INFO: create default config")
            cfg = default_config()
            with open(f"{config}", 'w+') as configfile:
                cfg.write(configfile)
            ctx.obj['config'] = cfg
            print(f"INFO: {config} config loaded")


def ask_parameter(value, name):
    if value is None:
        return input(f"{name} of disc?\n")
    else:
        return value

class Disc(yaml.YAMLObject):
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!disc'

    speed: float
    glide: float
    fade: float
    turn: float
    stability: float
    brand: str
    name: str

    def __init__(self, name, brand, speed, glide, fade, turn):
        self.name = name
        self.brand = brand
        self.speed = speed
        self.glide = glide
        self.fade = fade
        self.turn = turn

class DiscSet(yaml.YAMLObject):
    discs: list[Disc]
    name: str
    
    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!disc-set'

    def __init__(self, name):
        self.name = name
        self.discs = list()

    def add(self, disc: Disc):
        self.discs.append(disc)
   
    def number_of_discs(self):
        return len(self.discs)


class MyDiscs(yaml.YAMLObject):
    
    disc_sets: dict

    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!discnerd'

    def __init__(self):
        self.disc_sets = dict()

    def add_set(self, name):
        print("add_set")
        print(self.disc_sets)
        if not name in self.disc_sets:
            self.disc_sets[name] = DiscSet(name)
        else:
            print(f"INFO: disc set {name} already exists")

    def get_set(self, sname):
        if sname in self.disc_sets:
            return self.disc_sets[sname]
        else:
            return None

    def to_yaml(self):
        return yaml.dump(self.__dict__)

    def save(self, path):
        print("save")
        with open(expanduser(path), 'w+') as outfile:
            yaml.dump(self.__dict__, outfile)

    def load(self, path):
        try:
            print(f"INFO: try load data from {path}")
            with open(expanduser(path), 'r') as infile:
                data = yaml.safe_load(infile)
                self.__dict__.update(data) 
        except (OSError, IOError) as e:
            print("INFO: Initializing data from scratch")
            return MyDiscs()


@cli.command()
@click.pass_obj
@click.option('--name', required=True)
def add_set(ctx, name):
    data_path = ctx['config']['DEFAULT']['DataPath']
    try:
        myDiscs = MyDiscs()
        myDiscs.load(data_path)
        myDiscs.add_set(name)
        myDiscs.save(data_path)
        return True
    except:
        print("error")
        return False 


@cli.command()
@click.pass_obj
@click.option('--set', required=True)
@click.option('--name')
@click.option('--brand')
@click.option('--speed', type=float)
@click.option('--glide', type=float)
@click.option('--turn', type=float)
@click.option('--fade', type=float)
@click.option('--myid', type=float)
def add(ctx, set, name, brand, speed, glide, turn, fade, myid):

    data_path = ctx['config']['DEFAULT']['DataPath']

    myDiscs = MyDiscs()
    myDiscs.load(data_path)
    # Ask for missing Input
    name = ask_parameter(name, "name")
    brand = ask_parameter(brand, "brand")
    speed = ask_parameter(speed, "speed")
    glide = ask_parameter(glide, "glide")
    turn = ask_parameter(turn, "turn")
    fade = ask_parameter(fade, "fade")

    newDisc = Disc(name,brand,speed,glide,fade,turn)

    # generate id based on existing discs
    if myid is None:
        pass
   
    targetSet = myDiscs.get_set(set)
    if targetSet is None:
        print("ERROR: target set does not exist. create it with add-set")
        return
            
    targetSet.add(newDisc)   
    myDiscs.save(data_path)
    

if __name__ == '__main__':
    cli(obj={})