class Config:
    # Environment parameters
    Quantum = True
    temperature = 1.5 # K
    velocity_normal_ext = [0,0,0]
    velocity_super_ext = [0,0,0]

    # Vortex ring parameters
    center = [0,0,0]
    radius = 0.1 #cm = 1000um
    direction = "x"

    # Simulation parameters
    num_segments = 50
    iters = 10
    dt=1e-2
    method = "RK4"

    # Hyper-parameters
    BIOT = False
    min_seg_distance=20 #um
    max_seg_distance=200 #um
    max_shift = 5 #um

    # Output parameters
    plot_segments = True
    plot_segments_name = "Example of ring motion"
    plot_segments_save = False
    plot_velocities = False
    plot_velocities_name = "Example of velocities"
    plot_velocities_save = False
    graphs = 10
    reports = 10
