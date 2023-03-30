#!/bin/python3

import click
import yaml
import pickle
import configparser
import os
import pprint


from pathlib import Path
from os.path import expanduser

from .utils import  default_config
from .utils import load_config
from .utils import ask_parameter
from .data import Disc
from .data import DiscSet
from .data import MyDiscs

from .plot import plot_bar

DEFAULT_CONFIG_PATH = "~/.config/discnerd"
DEFAULT_CONFIG_NAME = "config"


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

@cli.group()
@click.pass_obj
def plot(ctx):
    pass


@plot.command()
@click.pass_obj
@click.option('--set', required=True)
def bar(ctx, set):
    data_path = ctx['config']['DEFAULT']['DataPath']
    myDiscs = MyDiscs()
    myDiscs.load(data_path)
    plot_bar(myDiscs.get_set(set))

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
@click.option('--myid', type=float, required=True)
def remove(ctx, set, myid):
    data_path = ctx['config']['DEFAULT']['DataPath']
    myDiscs = MyDiscs()
    myDiscs.load(data_path)
    myDiscs.get_set(set).remove(myid)
    myDiscs.save(data_path)

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


    targetSet = myDiscs.get_set(set)
    if targetSet is None:
        print("ERROR: target set does not exist. create it with add-set")
        return

    # generate id based on existing discs
    if myid is None:
        myid = targetSet.number_of_discs() + 1
   
    newDisc = Disc(name, brand, speed, glide, fade, turn, myid)
            
    targetSet.add(newDisc)   
    myDiscs.save(data_path)
    

if __name__ == '__main__':
    cli(obj={})