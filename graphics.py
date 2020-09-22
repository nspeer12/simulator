import tkinter as tk
import time
from ursina import *

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
    def __init__(self, master=None, height=80, width=80):
        super().__init__(master, width=width, height=height)
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
                time.sleep(0.5)



class Particle():
    def __init__(self, canvas, x1, y1, x2, y2, dy, dx, color="blue"):
        self.canvas = canvas
        self.particle = self.canvas.create_line(x1, y1, x2, y2, fill="blue")
        self.x1 = x1
        self.x2 = x2
        self.x = (x2-x1)/2
        self.y1 = y1
        self.y2 = y2
        self.y = (y2-y2)/2

        self.dy = dy
        self.dx = dx


    def move(self, dx, dy):
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

        self.canvas.move(self.particle, dx, dy)

    def scale(self, factor=1.1):
        self.x1 *= factor
        self.y1 *= factor
        self.x2 *= factor
        self.y2 *= factor


    def animation(self):
        frames = 10000
        i = 0
        while (i < frames):
            if (self.x1 > self.canvas.width or self.x1 <= 0):
                print("x hit")
                self.dx = -self.dx
                self.dy = -self.dy

            elif (self.y1 > self.canvas.height or self.y1 <= 0):
                print("y hit")
                self.dy = -self.dy
                self.dx = -self.dx

            print(self.x, self.y)
            self.move(self.dx, self.dy)
            self.canvas.move(self.particle, self.dx, self.dy)
            root.update()
            time.sleep(1/60)

            i += 1





if __name__== "__main__":
    root = tk.Tk()
    app = GraphicsCanvas(master=root, height=1000, width=1000)
    #app.draw_rect(500, 500, 600, 600)
    #app.animation()
    for i in range(100):
        electron = Particle(app, 500, 500, 600, 600, 5, 10)
        electron.animation()

    e2 = Particle(app, 800, 500, 300, 600)
    e2.animation()

    #app.animation()
    app.mainloop()
