from simulator import Simulator
from matplotlib.animation import FuncAnimation
from PIL import Image as im
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import os


img_dir = "imgs/"

def game_of_life():
    sim.shift()
    sim.print_matrix()
    time.sleep(0.1)


def update(i, show=False, save=True):
    sim.shift()

    frame = ax.imshow(sim.matrix)

    if save:
        fig.savefig(img_dir + "matrix_" + str(i) + ".png")


if __name__=="__main__":
    sim = Simulator(n=240)
    sim.seed_center()
    fig, ax = plt.subplots(figsize=(5,5))
    frame = ax.imshow(sim.matrix)
    animation = FuncAnimation(fig, update, interval=100)

    plt.show()
    #game_of_life()
