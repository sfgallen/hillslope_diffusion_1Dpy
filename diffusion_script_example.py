"""
This is a script that shows an example of how to run the 
simple_diffusion_model_py function that exicutes a finite difference
calculations to solve the transient linear diffusion equation used to model
hillslope diffusion.

Author: Sean F. Gallen
Date modified: 04/01/2021
Contact: sean.gallen[at]colostate.edu
"""

# Import libraries and functions
import numpy as np
import simple_diffusion_model_py as sdm

# generate distance and initial elevation profile (distance and elevation in m)
x = np.reshape(np.arange(0,100,1),(100,1))
y = np.zeros((len(x),1))
y[24:49] = np.sin(np.deg2rad(20))*x[0:25]
my = np.max(y)
y[49:74] = my + np.sin(np.deg2rad(-20))*x[0:25]

# assign inputs
k = 0.25            # diffusivity in m^2/kyr
run_time = 1000     # model run time on kyr
stabil = 1          # constant for numerical stability (increase if model blows up)
plot_opt = 1        # plot some results? 0 = no, 1 = yes.
U = 0.005           # uplift rate in m/kyr

# run the model
[yf] = sdm.simple_diffusion_model_py(x,y,k,run_time,U, stabil, plot_opt)
