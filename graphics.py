import tkinter as tk
import time
from ursina import *
import random

random.seed(1012520798)

class GraphicsFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master=master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")



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



class Particle():
    def __init__(self, canvas, x, y, r, dy, dx, color="blue"):
        self.canvas = canvas
        self.particle = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)
        self.x = x
        self.y = y
        self.r = r
        self.dy = dy
        self.dx = dx


    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.canvas.move(self.particle, dx, dy)

    def scale(self, factor=1.1):
        self.x *= factor
        self.y *= factor


    def bounce(self):
        frames = 10000
        i = 0
        offset = 250

        self.move(self.dx, self.dy)

        if (self.x >= 3*self.canvas.width/4):
            if (self.dx > 0):
                self.dx = -self.dx

            self.move(self.dx, self.dy)

        if (self.x < self.canvas.width/4):
            if (self.dx < 0):
                self.dx = -self.dx

        if (self.y > 3*self.canvas.height/4):
            if (self.dy > 0):
                self.dy = -self.dy

        if (self.y < self.canvas.height/4):
            if (self.dy < 0):
                self.dy = -self.dy

            self.move(self.dx, self.dy)

        #self.dy += 2



    def animation_step(self):
        self.canvas.move(self.particle, self.dx, self.dy)



if __name__== "__main__":

    root = tk.Tk()
    height = 1000
    width = 1000
    framerate=60

    app = GraphicsCanvas(master=root, height=height, width=width, bg="black")
    #app.draw_rect(500, 500, 600, 600)
    #app.animation()
    color = ["white", "green", "yellow", "red", "blue", "orange", "pink"]

    particles = []

    for i in range(100):
        #xi = random.randint(0, width)
        #yi = random.randint(0, height)
        xi = width / 2
        yi = width / 2
        dxi = random.randint(-10, 10) * random.random()
        dyi = random.randint(-10, 10) * random.random()
        r = random.randint(0,5)

        electron = Particle(app, xi, yi, r, dxi, dyi, color=random.choice(color))
        particles.append(electron)

    while True:
        for particle in particles:
            particle.animation_step()
            particle.bounce()


        root.update()
        time.sleep(1/framerate)
    #app.animation()
    app.mainloop()
