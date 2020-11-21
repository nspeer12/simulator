import tkinter as tk
import time
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
