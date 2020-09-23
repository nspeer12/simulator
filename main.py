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
from particle import *
import threading

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
    height = 1000
    width = 1000
    framerate=60

    app = GraphicsCanvas(master=root, height=height, width=width, bg="black")
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]

    particles = []

    for i in range(100):
        xi = width / 2
        yi = width / 2
        dxi = random.randint(-10, 10) * random.random()
        dyi = random.randint(-10, 10) * random.random()
        r = random.randint(0,5)

        ball = Particle(app, xi, yi, r, dxi, dyi, color=random.choice(color), charge=-10)
        particles.append(ball)


    while True:
        for particle in particles:
            particle.dy += 0.1
            particle.animation_step()
            particle.constrain()

        root.update()
        time.sleep(1/framerate)

    app.mainloop()

def collider(particles):
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]
    k = 2


    for i in range(0):
        xi = (engine.width / 2 + random.randint(-100,100))
        yi = (engine.height / 2 + random.randint(-100,100))
        dxi = 0
        dyi = 0
        r = random.randint(5,10)

        ball = Particle(engine.canvas, xi, yi, r, dxi, dyi, color=random.choice(color), charge=-100, mass=1e19)
        particles.append(ball)

    engine.update()

    input()

    i = 0
    while True:
        i += 1
        # shoot particle
        if i % 10 == 0:
            xi = 0
            yi = engine.height / 2
            dxi = 10
            dyi = 1
            r = random.randint(5,10)

            ball = Particle(engine.canvas, xi, yi, r, dxi, dyi, color="blue", charge=30, mass=1e25)
            particles.append(ball)

        if i % 10 == 0:
            xi = engine.width
            yi = engine.height / 2
            dxi = -10
            dyi = 1
            r = r

            ball = Particle(engine.canvas, xi, yi, r, dxi, dyi, color="red", charge=-30, mass=1e25)
            particles.append(ball)


        particles = coulomb(particles)

        for particle in particles:
            particle.constrain()

        for particle in particles:
            particle.step()

        engine.update()

def right_click(event):
    particles.append(Particle(engine.canvas, event.x, event.y, 10, 0, 0, color="blue", charge=-1e9, mass=1e20))
    engine.update()

def left_click(event):
    particles.append(Particle(engine.canvas, event.x, event.y, 10, 0, 0, color="red", charge=1e9, mass=1e20))
    engine.update()


def coulomb_helper(p, j):
    k = 1e5

    delta_y = j.y - p.y
    delta_x = j.x - p.x
    radius = math.sqrt(delta_x**2 + delta_y**2)

    # apply coulomb's law
    if radius != 0:
        if delta_x == 0:
            theta = 0
        else:
            theta = math.atan(delta_y/delta_x)

        force = (j.charge * p.charge * k) / radius**2

        #if p in visited:
        #    force = -force

        a_x = (force * math.cos(theta)) / p.mass
        a_y = (force * math.sin(theta)) / p.mass


        # inverse angle
        theta = theta - math.radians(0.5)

        if (p.charge * j.charge) > 0:
            force *= -1

        a_x = (force * math.cos(theta)) / j.mass
        a_y = (force * math.sin(theta)) / j.mass

        # handle positive and negative charges
        j.dx += a_x
        j.dy += a_y
        p.dx += a_x
        p.dy += a_y

        '''
        if (p.charge * j.charge) < 0:
            j.dx -= a_x
            j.dy -= a_y
            p.dx += a_x
            p.dy += a_y
        else:
            j.dx += a_x
            j.dy += a_y
            p.dx -= a_x
            p.dy -= a_y
        '''

def coulomb(particles):
    k = 1e5
    visited = []

    for particle in particles:
        particle.constrain()

        for p in particles:

            if p != particle and (particle, p) not in visited and (p, particle) not in visited:
                visited.append((particle, p))

                # lfgi
                threads = []
                for i in range(num_threads):
                    threads.append(threading.Thread(target=coulomb_helper, args=(particle, p)))

                for t in threads:
                    t.start()

        visited.append(particle)

    return particles


def collision(particles):
    visited = []

    for p in particles:
        for j in particles:
            if p != j and (j, p) not in visited and (p, j) not in visited:
                visited.append((j, p))
                # hashtag trig
                delta_y = j.y - p.y
                delta_x = j.x - p.x
                radius = math.sqrt(delta_x**2 + delta_y**2)

                if radius <= 5:
                    print("BOOM")

                    #particles.remove(p)
                    #particles.remove(j)

    return particles


def electro(particles):
    print(engine.width)
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]
    k = 10
    #engine.window.bind('<Motion>', click)
    #engine.window.mainloop()

    engine.update()

    i = 0
    while True:
        i += 1
        if i % 2 == 0 and i < 32:
            xi = (engine.width / 3 + random.randint(-100,100))
            yi = (engine.height / 2 + random.randint(-100,100))
            dxi = 0
            dyi = 0
            r = random.randint(5,10)

            electron = Particle(engine.canvas, xi, yi, r, dxi, dyi, color="blue", charge=-1e9, mass=1e20)
            particles.append(electron)

        if i % 2 == 0 and i < 32:
            xi = (2 * engine.width / 3 + random.randint(-100,100))
            yi = (engine.height / 2 + random.randint(-100,100))
            dxi = 0
            dyi = 0
            r = random.randint(5,10)

            proton = Particle(engine.canvas, xi, yi, r, dxi, dyi, color="red", charge=1e9, mass=1e20)
            particles.append(proton)

        particles = coulomb(particles)
        for particle in particles:
            particle.step()

        engine.update()

def test(particles):
    print(engine.width)
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]

    engine.update()

    electron = Particle(engine.canvas, 500, 100, 10, 0, 1, color="blue", charge=-1e9, mass=1e20)
    particles.append(electron)

    proton = Particle(engine.canvas, 520, 150, 10, 0, 0, color="red", charge=1e9, mass=1e20)
    particles.append(proton)

    while True:
        particles = coulomb(particles)
        #particles= collision(particles)
        for particle in particles:
            particle.step()
            #particle.trail()

        engine.update()


if __name__=="__main__":
    engine = Engine(width=1080, height=1080, framerate=15)
    engine.window.bind("<Button-1>", right_click)
    engine.window.bind("<Button-3>", left_click)
    engine.canvas.pack()

    num_threads = 16
    particles = []
    test(particles)
