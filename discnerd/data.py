import yaml
import os
from pathlib import Path
from os.path import expanduser


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
    id: int

    def __init__(self, name, brand, speed, glide, fade, turn, id):
        self.name = name
        self.brand = brand
        self.speed = speed
        self.glide = glide
        self.fade = fade
        self.turn = turn
        self.id = id
        self.stability = fade + turn

    def __repr__(self):
        return f"<Disc name: {self.name} brand:{self.brand} id:{self.id}>"

    def __str__(self):
        return f"<Disc name: {self.name} brand:{self.brand} id:{self.id}>"

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

    def remove(self, myid: int):
        self.discs = [d for d in self.discs if d.id != myid ]

    def number_of_discs(self):
        return len(self.discs)

    def get_discs(self) -> list[Disc]:
        return self.discs

    def __repr__(self):
        ret=""
        for d in self.discs:
            ret=f"{ret}\n{d}"
        return ret

    def __str__(self):
        ret=f"Discs ({self.number_of_discs()}):"
        for d in self.discs:
            ret=f"{ret}\n\t{d}"
        return ret


class MyDiscs(yaml.YAMLObject):
    
    disc_sets: dict

    yaml_loader = yaml.SafeLoader
    yaml_tag = u'!discnerd'

    def __init__(self):
        self.disc_sets = dict()

    def add_set(self, name):
        if not name in self.disc_sets:
            self.disc_sets[name] = DiscSet(name)
        else:
            print(f"INFO: disc set {name} already exists")

    def get_set(self, sname) -> DiscSet:
        if sname in self.disc_sets:
            return self.disc_sets[sname]
        else:
            return None

    def to_yaml(self):
        return yaml.dump(self.__dict__)

    def save(self, path):
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


