import matplotlib
import matplotlib.pyplot as plt

from .data import DiscSet
from .data import Disc
from math import floor 

def plot_bar(set: DiscSet):
    x_axis = ['7', '6', '5', '4', '3', '2', '1', '0', '-1', '-2', '-3', '-4']
    stabilities = {
        -4: 0,
        -3: 0,
        -2: 0,
        -1: 0,
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
    }
    for disc in set.get_discs():
        s = floor(disc.stability)
        stabilities[s] += 1
        
    y_axis = [
        stabilities[-4],
        stabilities[-3],
        stabilities[-2],
        stabilities[-1],
        stabilities[0],
        stabilities[1],
        stabilities[2],
        stabilities[3],
        stabilities[4],
        stabilities[5],
        stabilities[6],
        stabilities[7],
    ]
    plt.bar(x_axis, y_axis, color='g')
    plt.savefig("mygraph.png")