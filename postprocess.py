import numpy as np
import matplotlib.pyplot as plt

segs, vels0 = np.loadtxt('outs/velocites_0iters.txt', delimiter=",")

plt.figure(figsize=None)
plt.scatter(segs, vels0, color='blue')
#plt.scatter(segs, vels_100, color='red')
#plt.ylim(0.011, 0.015)
plt.show()



# Velocity evolution
# if cf.plot_velocities:
#     plt.figure()
#     plt.scatter(steps, velocities_real, label="Simulation")
#     plt.scatter(steps, velocities_theor, label="Theory")
#     plt.legend(loc=2)
#     plt.title(cf.plot_velocities_name)
#     plt.show()
#     if cf.plot_segments_save:
#         plt.savefig('screens/velocities.png')
