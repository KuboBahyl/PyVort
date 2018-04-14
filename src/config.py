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
    resolution = 60 #um
    epochs = 100
    dt=0.01
    method = "RK4"

    # Hyper-parameters
    BIOT = False
    LIA_updated = True
    min_seg_distance = 0.5 * resolution #um
    max_seg_distance = 2 * resolution #um
    max_shift = 1 #um

    # Output parameters
    plot_segments = True
    plot_segments_title = "Example of vortex re-segmentation"
    plot_segments_save = False
    if plot_segments_save:
        plot_segments_filename = "resegmentation"

    log_info = True

    plot_num = 10
    log_num = epochs/10
