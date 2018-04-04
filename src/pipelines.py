from main import main
from config import Config as cf

class Pipeline:
    def sanity_vel_vs_numseg():

        cf.plot_segments = False
        cf.log_info = False
        init_vels = []

        for i in range(10):
            cf.num_segments = (i+1)*10
            velocity = main(evolute=False, measure="velocity")
            init_vels.append(velocity)

        print(init_vels)


    def compare_vels():
        steps = []
        velocities_real = []
        velocities_theor = []

        velocity_real = vortex.velocity
        velocity_theory = calc_velocity_ring(vortex)

        steps.append(i)
        velocities_real.append(velocity_real)
        # velocities_theor.append(velocity_theory)
        pass

    def pass_test():
        cf.plot_segments = False
        cf.log_info = False

        quantity = main(measure="velocity",
                        evolute=False)
        print(quantity)

Pipeline.sanity_vel_vs_numseg()
