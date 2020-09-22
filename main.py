from simulator import Simulator
import matplotlib
from matplotlib.animation import FuncAnimation
from PIL import Image as im
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import os
import tkinter as tk
from datetime import datetime
from random import random
from graphics import *

random.seed(datetime.now())

img_dir = "imgs/"

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


def bounce():
    root = tk.Tk()
    height = 1000
    width = 1000
    framerate=60

    app = GraphicsCanvas(master=root, height=height, width=width, bg="black")
    #app.draw_rect(500, 500, 600, 600)
    #app.animation()
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]

    particles = []

    for i in range(10):
        #xi = random.randint(0, width)
        #yi = random.randint(0, height)
        xi = width / 2
        yi = width / 2
        dxi = random.randint(-10, 10) * random.random()
        dyi = random.randint(-10, 10) * random.random()
        r = random.randint(0,5)

        if (i % 2) == 0:
            electron = Particle(app, xi, yi, r, dxi, dyi, color=random.choice(color), charge=-1.6)
            particles.append(electron)
        else:
            proton = Particle(app, xi, yi, r, dxi, dyi, color=random.choice(color), charge=1.6)
            particles.append(proton)

    while True:
        for particle in particles:
            particle.animation_step()
            particle.bounce()
            particle.trail()

        root.update()
        time.sleep(1/framerate)
    #app.animation()
    app.mainloop()



def electro():
    root = tk.Tk()
    height = 1080
    width = 1080
    framerate=30

    # arbitrary Coulomb's constant
    k = 3

    app = GraphicsCanvas(master=root, height=height, width=width, bg="black")
    #app.draw_rect(500, 500, 600, 600)
    #app.animation()
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]

    particles = []

    for i in range(200):
        #xi = random.randint(0, width)
        #yi = random.randint(0, height)
        xi = width / 2 + random.randint(-10,10)
        yi = height / 2 + random.randint(-10,10)
        dxi = random.randint(-3,3) * random.random()
        dyi = random.randint(-3,3) * random.random()
        r = 3
        density = 1e10
        mass = (density * 4) / (3 * 3.141 * r**3)

        electron = Particle(app, xi, yi, r, dxi, dyi, mass=mass, color="blue", charge=-10000)
        particles.append(electron)


    while True:
        for particle in particles:
            for p in particles:
                if p != particle:
                    # hashtag trig
                    delta_y = particle.y - p.y
                    delta_x = particle.x - p.x
                    radius = math.sqrt(delta_x**2 + delta_y**2)

                    # prevent divide by zero error
                    if delta_x != 0:
                        theta = math.atan(delta_y/delta_x)
                    else:
                        theta = 0

                    # apply coulomb's law

                    if radius != 0:
                        force = (particle.charge * p.charge * k) / radius**2
                    else:
                        force = 0


                    a_x = (force * math.cos(theta)) / particle.mass
                    a_y = (force * math.sin(theta)) / particle.mass
                    particle.dx += a_x
                    particle.dy += a_y


            particle.constrain()
            particle.animation_step()



        root.update()
        time.sleep(1/framerate)

    app.mainloop()


if __name__=="__main__":
    electro()
