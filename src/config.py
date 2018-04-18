class Config:
    # Environment parameters
    is_temp_zero = False
    if not is_temp_zero:
        temperature = 1.5 # K

    velocity_normal_ext = [0,0,0] # no source
    velocity_super_ext = [0,0,0] # no source

    # Vortex ring parameters
    is_ring = True # don't change
    if is_ring:
        center = [0,0,0] # um
        radius = 1000 # um
        direction = "x"

    # Simulation parameters
    resolution = 60 # um
    epochs = 10
    dt=0.01 # starting
    method = "RK4" # or "euler"
    use_BIOT = False
    use_LIA_updated = True

    # Hyper-parameters
    length_max_error = 0.01 # in percents
    min_num_seg = 4 # smaller vortex than this is killed
    min_seg_distance = 0.5 * resolution # um
    max_seg_distance = 2 * resolution # um
    max_shift = 1 # um

    # Output parameters
    plot_segments = True
    plot_segments_title = "Example of vortex"
    plot_segments_save = False
    if plot_segments_save:
        plot_segments_filename = "resegmentation"

    log_info = True

    plot_num = 10
    log_num = 10
