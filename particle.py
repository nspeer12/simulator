class Particle():
    def __init__(self, canvas, x, y, r, dx, dy, color="blue", charge=0, mass=10):
        self.canvas = canvas
        self.particle = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color)
        self.x = x
        self.y = y
        self.r = r
        self.dy = dy
        self.dx = dx
        self.charge=charge
        self.mass = mass
        self.color = color
        self.prev_x = x
        self.prev_y = y
        self.light_trail = []

    def step(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x += self.dx
        self.y += self.dy
        self.canvas.move(self.particle, self.dx, self.dy)


    def scale(self, factor=1.1):
        self.x *= factor
        self.y *= factor

    def delete(self):
        self.canvas.delete(self.particle)
        
    def trail(self):
        if len(self.light_trail) > 10:
            self.canvas.delete(self.light_trail.pop(0))

        self.light_trail.append(self.canvas.create_line(self.prev_x, self.prev_y, self.x, self.y, fill=self.color))


    def constrain(self):
        alpha = 0.7
        if (self.x >= self.canvas.width):
            if (self.dx > 0):
                self.dx = -self.dx * alpha

        if (self.x <= 0):
            if (self.dx < 0):
                self.dx = -self.dx * alpha

        if (self.y > self.canvas.height):
            if (self.dy > 0):
                self.dy = -self.dy * alpha

        if (self.y <= 0):
            if (self.dy < 0):
                self.dy = -self.dy * alpha
