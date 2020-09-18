import numpy as np
from simulator import Simulator

if __name__=="__main__":
    sim = Simulator()
    sim.randomize_matrix()
    sim.plot_matrix()
