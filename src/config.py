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
    num_segments = 100
    iters = 10
    dt=0.01
    method = "RK4"

    # Hyper-parameters
    BIOT = False
    min_seg_distance = 0 #um
    max_seg_distance = 10000 #um
    max_shift = 1 #um

    # Output parameters
    plot_segments = True
    plot_segments_name = "Example of ring motion"
    plot_segments_save = False
    plot_velocities = False
    plot_velocities_name = "Example of velocities"
    plot_velocities_save = False

    log_info = True

    graphs = 10 if plot_segments else 0
    reports = 10 if log_info else 0
