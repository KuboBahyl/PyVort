from main import main
from config import Config as cf
import numpy as np
from tqdm import tqdm

cf.plot_segments = False
cf.log_info = False

class Pipeline:
    def sanity_quantum(iters):
        cf.iters = iters
        velocities = []

        for cf.Quantum in [True, False]:
            velocities = main(evolute=True, dynamic_quantity_name="velocity")
            energies = main(evolute=True, dynamic_quantity_name="calc_energy_ring")

            np.savetxt('outs/velocites_Quant-{}.txt'.format(cf.Quantum), velocities, delimiter=',')
            np.savetxt('outs/energies_Quant-{}.txt'.format(cf.Quantum), energies, delimiter=',')

        print("Files with velocities and energies created!")

    def sanity_vel_vs_numseg(num_segs):
        cf.iters = 100
        vels_init = []
        vels_100step = []

        num_seg_arr = np.linspace(10,200,num_segs)

        for num in num_seg_arr:
            cf.num_segments = int(num)

            velocity = main(evolute=False, static_quantity_name="velocity")
            vels_init.append(velocity)

            velocity = main(evolute=True, static_quantity_name="velocity")
            vels_100step.append(velocity)

        np.savetxt('outs/velocites_0iters.txt', vels_init, delimiter=',')
        np.savetxt('outs/velocites_100iters.txt', vels_100step, delimiter=',')


    def compare_vels():
        steps = []
        velocities_real = []
        velocities_theor = []

        velocity_real = vortex.velocity
        velocity_theory = calc_velocity_ring(vortex)

        steps.append(i)
        velocities_real.append(velocity_real)
        # velocities_theor.append(velocity_theory)

        # Velocity evolution
        if cf.plot_velocities:
            plt.figure()
            plt.scatter(steps, velocities_real, label="Simulation")
            plt.scatter(steps, velocities_theor, label="Theory")
            plt.legend(loc=2)
            plt.title(cf.plot_velocities_name)
            plt.show()
            if cf.plot_segments_save:
                plt.savefig('screens/velocities.png')

    def pass_test():
        cf.plot_segments = False
        cf.log_info = False

        quantity = main(measure="velocity",
                        evolute=False)
        print(quantity)

#Pipeline.sanity_vel_vs_numseg(num_segs=5)
Pipeline.sanity_quantum(iters=5)
