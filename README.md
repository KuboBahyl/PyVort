# Simulations of vortex dynamics in superfluid

`Pyvort` is a new platform
to simulate quantum vortex rings. The code is written in well commented Python 3, arranged in a modular structure. All source files are located in `src/` folder and the example pictures in `graphics/`.

All physical and numeric motivations can be found in `readme.pdf`. This report was created for the Student conference 2018 in FMFI UK.

To run the simulation with default settings, execute:

`python src/main.py`

## Attributes:

All vortex ring properties are pre-set in `config.py` file with following attributes:

* ### Physics:
  **Temperature** - we support temperatures from 1.0K to 2.10K with 0.1K stepping

  **External sources** - constant 3D vector fields of normal and supefluid velocity

  **Ring properties** - center location, radius and normal direction of vortex ring

* ### Global:
  **Resolution** - initial distance between two neighboring segments

  **Epochs & time-step** - number and initial length of time step

  **Time-step method** - choose between *Euler* and *Runge-Kutta4*

  **Velocity method** - choose whether velocity should be calculated via updated LIA method or BIOT method or neither of them

* ### Hyper-params:
  **Lenght and segment error** - set maximum error of vortex length and minimum number of segments in purpose to kill the simulation

  **Minimal and maximal distance** - set the range for neighboring segment distance

  **Maximal shift** - set the maximal spatial shift of vortex ring in a single step

* ### Output settings:
  **Plot settings** - choose whether to plot, how much plot and whether save the vortex ring simulation

  **Log settings** - choose whether and how much log in console during simulation


Config file `config.py` is pre-set on standard simulation values (temperature 1.5K, no sources, radius of 1000um, resolution 60um, 100 epochs, 0.01s initial time-step, RK4 and LIA updated method, 1% length error, plot 10 simulation states and log every 10th step).
