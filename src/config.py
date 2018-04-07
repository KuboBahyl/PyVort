class Config:
    # Environment parameters
    temp_zero = False
    if not temp_zero:
        temperature = 1.5 # K
    velocity_normal_ext = [0,0,0]
    velocity_super_ext = [0,0,0]

    # Vortex ring parameters
    center = [0,0,0]
    radius = 1000 #um
    direction = "x"

    # Simulation parameters
    resolution = 30 #um
    epochs = 100
    dt=0.01
    method = "RK4"

    # Hyper-parameters
    BIOT = False
    LIA_updated = True
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

    plot_num = 10 if plot_segments else 0
    log_num = 10 if log_info else 0
