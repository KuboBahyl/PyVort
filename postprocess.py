import numpy as np
import matplotlib.pyplot as plt

def process_quantum():
    epochs, vels_Qfalse = np.loadtxt('outs/velocites_Quant-False.txt', delimiter=",")
    epochs, vels_Qtrue = np.loadtxt('outs/velocites_Quant-True.txt', delimiter=",")
    epochs, eners_Qfalse = np.loadtxt('outs/energies_Quant-False.txt', delimiter=",")
    epochs, eners_Qtrue = np.loadtxt('outs/energies_Quant-True.txt', delimiter=",")

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.scatter(epochs, 10**4*vels_Qtrue, color='green', marker=".", label='v_Quant=True')
    ax1.plot(epochs, 10**4*vels_Qfalse, 'g--', label='v_Quant=False')
    ax1.legend(loc="center left")
    ax1.set_xlabel('Number of epochs')
    ax1.set_ylabel('Center velocity [$\mu$m/s]')
    ax1.set_ylim(130,141)

    ax2.scatter(epochs, eners_Qtrue/10**6, color='blue', marker=".", label='E_Quant=True')
    ax2.plot(epochs, eners_Qfalse/10**6, 'b--', label='E_Quant=False')
    ax2.set_ylabel('Ring energy [MeV]')
    ax2.legend(loc="center right")

    plt.title('Quantum effect on velocity and energy')

    plt.savefig('outs/quantum.pdf')
    #plt.show()


def process_vels():
    res, vels0 = np.loadtxt('outs/velocites_0epochs.txt', delimiter=",")
    res, vels100 = np.loadtxt('outs/velocites_100epochs.txt', delimiter=",")

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.scatter(res, 10**4*vels0, color='blue', label='v_init')
    ax1.legend(loc="upper left")
    ax1.set_ylabel('Center velocity [$\mu$m/s]')
    ax1.set_xlabel('Resolution [$\mu$m]')

    ax2.scatter(res, 10**4*vels100, color='red', label='v_100steps')
    ax2.legend(loc="upper right")

    plt.title('Velocity distributions of vortex ring')

    plt.savefig('outs/velocities.pdf')
    #plt.show()

def process_stability():
    res, max_epoch500 = np.loadtxt('outs/maxepochs_radius500um.txt', delimiter=",")
    res, max_epoch1000 = np.loadtxt('outs/maxepochs_radius1000um.txt', delimiter=",")
    res, max_epoch2000 = np.loadtxt('outs/maxepochs_radius2000um.txt', delimiter=",")

    plt.figure()
    plt.scatter(res, max_epoch500/1000, color='green', label='radius=500um')
    plt.scatter(res, max_epoch1000/1000, color='blue', marker=",", label='radius=1000um')
    plt.scatter(res, max_epoch2000/1000, color='red', marker="x", label='radius=2000um')
    plt.legend(loc="lower right")

    plt.xlabel('Resolution [$\mu$m]')
    plt.ylabel('Maximal reached epoch [in thousands]')
    plt.title('Stability of Euler method')

    plt.savefig('outs/stability.pdf')
    #plt.show()

process_vels()

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
