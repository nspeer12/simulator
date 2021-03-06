# simulator

### 2D physics simulator
Implemented in `numpy` and visualized using `tkinter`

Visualize physical phenomenom at a macro and micro level. See concepts such as Newton's law affect particles at a macro level, and charged particles interact on an atomic level.

*Note: I made this at 4 a.m. so please excuse any issues. Feel free to contribute or report any issues.*

## How to Run

For instructions run `python main.py --help`

To try out some demos run `python main.py --demo <1-3>`


### Graphics

The Graphics class is a wrapper on `tk.Tk()` that allows for real-time visualization of the simulator. The graphics engine draws, updates, and displays what's going on in the simulator.

#### Bouncy Balls

Watch gravity come to life as it pulls down on balls of different shapes and sizes

<img style="height:250px; width:250px;" src="renders/bounce.gif">

#### Coulomb's Law

Visualize charged particles interacting in an electric field

<img style="height:250px; width:250px;" src="renders/coulomb.gif">


#### Click to add more particles

<img style="height:250px; width:250px;" src="renders/click.gif">

### Particle

Particle is the most basic object in the simulation. It controls the shape, size, and behaviour of particles contained in the Simulator or Graphics engine. It contains variables such as x and y position, mass, charge, velocity and acceleration.

### Simulator

Simulator is a class that uses 2D `numpy` arrays as a representation of physical space. Particles can live in the simulation. A variety of physical and mathematical concepts can be applied onto the entire simulation, such as gravity or an electromagnetic field. Simulator can also display a variety of math-art, like the the transformation of matricies to into geometric snowflakes.

<img style="height:250px; width:250px;" src="renders/flower0.gif">


