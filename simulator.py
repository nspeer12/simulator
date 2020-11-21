import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math


np.random.seed(8234535)
np.printoptions(precision=3, supress=True)


class Simulator:
    def __init__(self, n=300, dim=2):
        self.n = n
        self.dim = dim
        self.size = tuple([n for i in range(dim)])
        self.matrix = np.zeros(self.size)
        self.history = []

    def print_matrix(self):
        print(self.matrix)

    def randomize_matrix(self):
        for j in range(self.n):
            for i in range(self.n):
                self.matrix[i][j] = np.random.randint(0,255)

    def zero_matrix(self):
        self.matrix = np.zeros(self.size)

    def plot_matrix(self):
        if self.dim == 2:
            plt.imshow(self.matrix)
            plt.show()

    def matrix_to_img(self, x, dir_name="imgs/"):
        im = Image.fromarray(np.uint8(self.matrix))
        im.save(dir_name + "matrix_" + str(x) + ".jpg")


    def seed_matrix(self, num_seeds=100):
        # place random values into simulator

        # prevent overflow
        num_seeds %= self.n * self.n

        for k in range(num_seeds):
            i = np.random.randint(0, self.n - 1)
            j = np.random.randint(0, self.n - 1)

            # assign binary digit to seeded choice
            self.matrix[i][j] = np.random.randint(2)

    def seed_center(self):
        i = math.floor(self.n/2)
        self.matrix[i][i] = 1


    def record_instance(self):
        self.history.append(self.matrix)


def update(i, show=False, save=True):
    sim.flower()

    frame = ax.matshow(sim.matrix)
    fig.canvas.flush_events()

    if save:
        fig.savefig(img_dir + "matrix_" + str(i) + ".png")


def animation():
    sim = Simulator(n=240)
    sim.seed_center()
    fig, ax = plt.subplots(figsize=(10,10))
    plt.axis("off")
    frame = ax.matshow(sim.matrix)
    animation = FuncAnimation(fig, update, interval=500, save_count=50)
    plt.show()

def update_history(i, show=False, save=False):
    matrix = sim.history[i]

    im.set_data(matrix)
    #im = ax.matshow(matrix)
    #fig.canvas.flush_events()

    if save:
        plt.savefig(img_dir + "matrix_" + str(i) + ".png")

    return im

def animate_history(sim, frames):
    animation = FuncAnimation(fig, update_history, interval=500, save_count=50, frames=frames)

    Writer = matplotlib.animation.writers["ffmpeg"]
    writer = Writer(fps=15, bitrate=1800)
    animation.save("game_of_life.mp4", writer=writer)
    plt.show()

def flower_0(sim):
    next = np.copy(sim.matrix)
    next += np.roll(sim.matrix, 1, axis=0)
    next += np.roll(sim.matrix, 1, axis=1)
    next += np.roll(sim.matrix, -1, axis=0)
    next += np.roll(sim.matrix, -1, axis=1)
    #next += np.roll(sim.matrix, -1, axis=(0,1))
    #next += np.roll(sim.matrix, 1, axis=(0,1))
    sim.matrix = next
    sim.matrix %= 4
    sim.record_instance()
    return sim.matrix

def snowflake(sim):
    next = np.copy(sim.matrix)
    next += np.roll(sim.matrix, 1, axis=0) % 2
    next += np.roll(sim.matrix, 1, axis=1) % 2
    next += np.roll(sim.matrix, -1, axis=0) % 2
    next += np.roll(sim.matrix, -1, axis=1) % 2
    next += np.roll(sim.matrix, -1, axis=(0,1))
    next += np.roll(sim.matrix, 1, axis=(0,1))
    next %= 30

    return next

def game_of_life(sim):

    n = sim.n
    matrix = sim.matrix

    for j in range(n):
        for i in range(n):
            neighbors = 0
            # up
            if i > 0:
                neighbors += matrix[i-1][j]

            # up & right
            if i > 0 and j < n-1:
                neighbors += matrix[i-1][j+1]

            # right
            if j < n-1:
                neighbors += matrix[i][j+1]

            # down & right
            if j < n-1 and i < n-1:
                neighbors += matrix[i+1][j+1]

            # down
            if i > n-1:
                neighbors += matrix[i+1][j]

            # down & left
            if i < n-1 and j > 0:
                neighbors += matrix[i+1][j-1]

            # left
            if j > 0:
                neighbors += matrix[i][j-1]

            # left & up
            if j > 0 and i > 0:
                neighbors += matrix[i-1][j-1]

            # update state

            # not enough neighbors
            if neighbors < 2:
                matrix[i][j] = 0

            # too many neighbors
            if neighbors > 3:
                matrix[i][j] = 0

            # new cell
            if neighbors == 3:
                matrix[i][j] = 1

    return matrix


