
# criterium: vortex length error over 1%
# fixed: euler method, temperature, Quantum, dt!!! (it will adtapt to situation)
# higher temperatures are weakly more stable
# BIOT term makes it far more stable!

# Exp Paper: R lies between 5um and 100um
# Sim Paper: R = 0.1cm = 1000um
# Tree Paper: R = 0.02cm = 200um

radii = [0.01, 0.1]
stability = [
    {'radius': 0.001, #10um
    'num_seg': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'iters': [16, 10, 8, 7, 7, 6, 6, 6, 5, 5]}
    ,
    {'radius': 0.01, #100um
    'num_seg': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'iters': [140, 33, 19, 14, 12, 11, 10, 9, 8, 8]}
    ,
    {'radius': 0.1, #1000um
    'num_seg': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'iters': [2500, 1050, 255, 100, 55, 35, 28, 22, 19, 17]}
]

# maximum stability without resegmentation

num_seg = [80, 100]
iters = [3500, 2600]
