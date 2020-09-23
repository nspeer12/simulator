import tkinter as tk
import time
from ursina import *
import random
import math
from datetime import datetime
from particle import *
random.seed(datetime.now())


class Engine():
    def __init__(self, height=1080, width=1920, framerate=60):
        self.window = tk.Tk()
        self.height = height
        self.width = width
        self.framerate = framerate
        self.canvas = GraphicsCanvas(master=self.window, height=height, width=width, bg="black")

    def update(self):
        self.window.update()
        time.sleep(1/self.framerate)

class GraphicsCanvas(tk.Canvas):
    def __init__(self, master=None, height=80, width=80, bg="black"):
        super().__init__(master, width=width, height=height, bg=bg)
        self.width = width
        self.height = height
        self.master = master

        # store shapes
        self.shapes = []
        self.pack()

    def draw_line(self):
        y = int(self.height / 2 )
        self.create_line(0, y, self.width, y, fill="#476042")


    def draw_rect(self, x1, y1, x2, y2):
        self.shapes.append(self.create_rectangle(x1, y1, x2, y2, fill="black"))

    def animation(self):
        for i in range(100):
            for shape in self.shapes:
                self.move(shape, 5, 5)




if __name__== "__main__":

    root = tk.Tk()
    height = 2160
    width = 3840
    framerate=60

    app = GraphicsCanvas(master=root, height=height, width=width, bg="black")
    #app.draw_rect(500, 500, 600, 600)
    #app.animation()
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]

    particles = []

    for i in range(10000):
        #xi = random.randint(0, width)
        #yi = random.randint(0, height)
        xi = width / 2
        yi = width / 2
        dxi = random.randint(-10, 10) * random.random()
        dyi = random.randint(-10, 10) * random.random()
        r = random.randint(0,5)

        if i % 2 == 0:
            electron = Particle(app, xi, yi, r, dxi, dyi, color=random.choice(color), charge=-10)
            particles.append(electron)
        else:
            protom = Particle(app, xi, yi, r, dxi, dyi, color=random.choice(color), charge=10)
            particles.append(proton)

    while True:
        for particle in particles:
            particle.animation_step()
            particle.bounce()

            if particle.x > width or particle.x < 0 or particle.y > height or particle.y < 0:
                particles.remove(particle)

            for p in particles:
                if p != particle:
                    # hashtag trig
                    delta_y = particle.y - p.y
                    delta_x = particle.x - p.x
                    radius = math.sqrt(delta_x**2 + delta_y**2)

                    # scale factor
                    alpha = 0.01

                    # apply coulomb's law
                    if radius != 0:

                        if delta_x != 0:
                            theta = math.atan(delta_y/delta_x)

                        force = (particle.charge * p.charge * k) / (radius*alpha)**2
                        a_x = (force * math.cos(theta)) / particle.mass
                        a_y = (force * math.sin(theta)) / particle.mass
                        particle.dx += a_x
                        particle.dy += a_y
                    else:
                        particle.dx = 0
                        particle.dy = 0


        root.update()
        time.sleep(1/framerate)

    #app.animation()
    app.mainloop()
