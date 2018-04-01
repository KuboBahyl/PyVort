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
    dt=1e-2
    method = "RK4"

    # Hyper-parametes
    BIOT = False
    min_seg_distance=50 #um
    max_seg_distance=100 #um

    # Output parameters
    max_plot_shift = 5 #um
    graphs = 10
    reports = 10
