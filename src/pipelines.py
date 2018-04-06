from main import main
from config import Config as cf
import numpy as np
from tqdm import tqdm

cf.plot_segments = False
cf.log_info = False

class Pipeline:
    def sanity_quantum(epochs):
        cf.epochs = epochs
        velocities = []

        epoch_list = np.linspace(0,epochs-1,epochs)

        for cf.Quantum in [True, False]:
            velocities = main(evolute=True, dynamic_quantity_name="velocity")
            energies = main(evolute=True, dynamic_quantity_name="calc_energy_ring")

            np.savetxt('outs/velocites_Quant-{}.txt'.format(cf.Quantum), (epoch_list, velocities), delimiter=',', fmt='%.5e')
            np.savetxt('outs/energies_Quant-{}.txt'.format(cf.Quantum), (epoch_list, energies), delimiter=',', fmt='%.5e')

        print("Files with velocities and energies created!")

    def sanity_vel_vs_numseg(res_num):
        vels_init = np.zeros(res_num)
        vels_100step = np.zeros(res_num)

        res_arr = np.linspace(40,200,res_num)

        for i in range(res_num):
            res = res_arr[i]
            cf.resolution = res

            vels_init[i] = main(evolute=False, static_quantity_name="velocity")
            cf.epochs = 100
            vels_100step[i] = main(evolute=True, static_quantity_name="velocity")

        np.savetxt('outs/velocites_0epochs.txt', (res_arr, vels_init), delimiter=',', fmt='%.5e')
        np.savetxt('outs/velocites_100epochs.txt', (res_arr, vels_100step), delimiter=',', fmt='%.5e')

        print("Files with velocities created!")

    def stability(res_num):
        radii = [500, 1000, 2000]
        res_arr = np.linspace(40,200,res_num)

        cf.log_info = True
        cf.log_num = 100
        cf.method = "euler"
        cf.epochs = 10**4

        for radius in radii:
            cf.radius = radius
            epochs_max = np.zeros(res_num)

            for i in range(res_num):
                res = res_arr[i]
                cf.resolution = res
                epochs_max[i] = main(evolute=True, static_quantity_name="epoch")

            np.savetxt('outs/maxepochs_radius{}um.txt'.format(radius), (res_arr, epochs_max), delimiter=',', fmt='%.5e')

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

#Pipeline.sanity_quantum(epochs=1000)
#Pipeline.sanity_vel_vs_numseg(res_num=33) # changing res by 5
Pipeline.stability(res_num=17)
