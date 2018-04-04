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

        iter_list = np.linspace(0,iters,iters)

        for cf.Quantum in [True, False]:
            velocities = main(evolute=True, dynamic_quantity_name="velocity")
            energies = main(evolute=True, dynamic_quantity_name="calc_energy_ring")

            np.savetxt('outs/velocites_Quant-{}.txt'.format(cf.Quantum), (iter_list, velocities), delimiter=',')
            np.savetxt('outs/energies_Quant-{}.txt'.format(cf.Quantum), (iter_list, energies), delimiter=',')

        print("Files with velocities and energies created!")

    def sanity_vel_vs_numseg(num_segs):
        cf.iters = 100
        vels_init = np.zeros(num_segs)
        vels_100step = np.zeros(num_segs)

        num_seg_arr = np.linspace(10,100,num_segs)

        for i in range(num_segs):
            num = num_seg_arr[i]
            cf.num_segments = int(num)

            vels_init[i] = main(evolute=False, static_quantity_name="velocity")
            vels_100step[i] = main(evolute=True, static_quantity_name="velocity")

        np.savetxt('outs/velocites_0iters.txt', (num_seg_arr, vels_init), delimiter=',')
        np.savetxt('outs/velocites_100iters.txt', (num_seg_arr, vels_100step), delimiter=',')

        print("Files with velocities created!")

    def stability(num_segs):
        radii = [0.001, 0.01, 0.1, 1]
        num_seg_arr = np.linspace(10,100,num_segs)

        cf.log_info = True
        cf.log_num = 1000
        cf.method = "euler"
        cf.iters = 10**5

        for radius in radii:
            cf.radius = radius
            epochs_max = np.zeros(num_segs)

            for i in range(num_segs):
                num = num_seg_arr[i]
                cf.num_segments = int(num)
                epochs_max[i] = main(evolute=True, static_quantity_name="epoch")

            np.savetxt('outs/maxiters_radius{}cm.txt'.format(radius), (num_seg_arr, epochs_max), delimiter=',')

        print("Files saved!")

    def compare_vels():
        steps = []
        velocities_real = []
        velocities_theor = []

        velocity_real = vortex.velocity
        velocity_theory = calc_velocity_ring(vortex)

        steps.append(i)
        velocities_real.append(velocity_real)
        # velocities_theor.append(velocity_theory)

    def pass_test():
        cf.plot_segments = False
        cf.log_info = False

        quantity = main(measure="velocity",
                        evolute=False)
        print(quantity)

#Pipeline.sanity_vel_vs_numseg(num_segs=2)
#Pipeline.sanity_quantum(iters=5)
Pipeline.stability(num_segs=2)
