# simulator

### 2D physics simulator
Implemented in `numpy` and visualized using `tkinter`

Visualize physical phenomenom at a macro and micro level. See concepts such as Newton's law affect particles at a macro level, and charged particles interact on an atomic level.



## How to Run

For instructions run `python main.py --help`

To try out some demos run `python main.py --demo <1-3>`


### Simulator

Simulator is a class that uses 2D `numpy` arrays as a representation of physical space. Particles can live in the simulation. A variety of physical and mathematical concepts can be applied onto the entire simulation, such as gravity or an electromagnetic field. Simulator can also display a variety of math-art, like the the transformation of matricies to into geometric snowflakes.

### Graphics

The Graphics class is a wrapper on `tk.Tk()` that allows for real-time visualization of the simulator. The graphics engine draws, updates, and displays what's going on in the simulator.

### Particle

Particle is the most basic object in the simulation. It controls the shape, size, and behaviour of particles contained in the Simulator or Graphics engine. It contains variables such as x and y position, mass, charge, velocity and acceleration.

