"""
simple_diffusion_model_py.py will simulate linear hillslope diffusion given an
intial and final topographic profile using inputs of a diffusion parameter, k,
and a model run time. The code evolves the topograpy using explicit finitie
difference.

Required inputs:
    x - distance along the profile (note distance vector should have even increments)
    y - elevation in meters of the intial topographic profile
    k - diffusion coefficient in m^2/kyr
    run_time - total model run time in kyr
    
Optional inputs:
    U - uplift rate in m/kyr. default = 0
    stabil - parameter for numerical stability (increase if model blows up). default = 1
    plot_opt - plot results? 0 if no, 1 if yes. 0 is the default

Outputs:
    y_mod - elevation in final model timestep
    
Examples:
    

Author: Sean F. Gallen
Date Modified: 03/31/2021
contact: sean.galen[at]colostate.edu
"""

# import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.pylab import pl

def simple_diffusion_model_py(x,y,k,run_time,U = 0, stabil = 1, plot_opt = 0):
    
    # define dx (note, this assume uniformly space vector)
    dx = x[1]-x[0]
    
    # determine stable model time step that satifies the CLF condition
    lam = 0.4/stabil
    dt = lam*dx**2/k
    
    # use dt and run_time to generate the time vector
    #t = np.arange(0,run_time,dt)
    t_steps = int(np.ceil(run_time/dt))
    
    # generate a padded array to avoid edge effects
    y_pad = np.zeros((len(y)+2,1))
    y_pad[0] = y[0]
    y_pad[len(y_pad)-1] = y[len(y)-1]
    
    # set boundary and initial conditions
    y_s = y[0]
    y_e = y[len(y)-1]
    yt = y
    
    # if plotting generate the initial plot
    if plot_opt == 1:
        # pick figure sze
        plt.figure(figsize = (5,3))
        nplots = 10
        t_plots = int(np.ceil(t_steps/nplots))
        #plott = np.round(len(t)/nplots)
        cols = plt.cm.cividis(np.linspace(0,1,nplots))
        plt.plot(x,y,'k-',linewidth = 2)
        plt.xlabel('Distance (m)')
        plt.ylabel('Elevation (m)')
        plt.tick_params(direction='in')
        nn = 0
    
    # run the time loop
    for ti in range(t_steps):
        
        # calculate curvature
        C = (y_pad[2:] - 2*y_pad[1:-1] + y_pad[0:-2])*lam;
        
        # evolve the profile
        yt = yt + C + U*dt
        
        # deal with boundaries and reset padded array
        yt[0] = y_s
        yt[len(yt)-1] = y_e
        y_pad[1:-1] = yt
        
        # plot the results if needed
        if plot_opt == 1:
            #if ti >= plott*n:
            if   np.remainder(ti,t_plots) == 0:
                plt.plot(x,yt,'-',color = cols[nn], linewidth = 0.5)
                nn = nn + 1
                #print(nn)
    
    # plot the final profile if needed
    if plot_opt == 1:
        # plot the final timestep
        plt.plot(x,yt,'k--',linewidth = 2)
    
    # output the final elevation
    return[yt]