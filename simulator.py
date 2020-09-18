import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math


np.random.seed(8234535)
np.printoptions(precision=3, supress=True)


class Simulator:
    def __init__(self, n=100, dim=2):
        self.n = n
        self.dim = dim
        self.size = tuple([n for i in range(dim)])
        self.matrix = np.zeros(self.size)

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

    def shift(self):
        self.matrix -= np.roll(self.matrix, 1, axis=0)
        self.matrix -= np.roll(self.matrix, 1, axis=1)
        self.matrix += np.roll(self.matrix, -1, axis=0)
        self.matrix += np.roll(self.matrix, -1, axis=1)

        self.matrix %= 255

        self.matrix += self.matrix.T
