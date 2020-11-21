from simulator import Simulator
import matplotlib
from matplotlib.animation import FuncAnimation
from PIL import Image as im
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time
import os
import sys
import tkinter as tk
from datetime import datetime
from random import random
from graphics import *
from particle import *
import threading

random.seed(datetime.now())

img_dir = "imgs/"


def bounce(particles):
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]

    for i in range(100):
        xi = engine.width / 2
        yi = engine.width / 2
        dxi = random.randint(-10, 10) * random.random()
        dyi = random.randint(-10, 10) * random.random()
        r = random.randint(0,5)

        ball = Particle(engine.canvas, xi, yi, r, dxi, dyi, color=random.choice(color), charge=-10)
        particles.append(ball)


    while True:
        for particle in particles:
            particle.dy += 0.1
            particle.step()
            particle.constrain()
       
        engine.update()
       
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
    
    print('         _                 __      __            ')
    print('   _____(_)___ ___  __  __/ /___ _/ /_____  _____')
    print('  / ___/ / __ `__ \/ / / / / __ `/ __/ __ \/ ___/')
    print(' (__  ) / / / / / / /_/ / / /_/ / /_/ /_/ / /    ')
    print('/____/_/_/ /_/ /_/\__,_/_/\__,_/\__/\____/_/     ')
    print()

    if len(sys.argv) > 1:
        if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
            print('Usage:')
            print('help menu: -h or --help')
            print('try demos: --demo <1-3>')
        elif '--demo' in sys.argv:
            try:
                index = sys.argv.index('--demo')
            except:
                pass
            else:
                if index:
                    demo = sys.argv[index+1]
                    print(demo)
                    engine = Engine(width=500, height=500, framerate=15)
                    engine.window.bind("<Button-1>", right_click)
                    engine.window.bind("<Button-3>", left_click)
                    engine.canvas.pack()
                    num_threads = 16
                    particles = []
             
                    if demo == "1":
                        electro(particles)
                    elif demo == "2":
                        bounce(particles)
                    elif demo == "3":
                        test(particles)
     
