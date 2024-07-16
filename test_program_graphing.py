import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# 50x50 100 sensors, rs = 10 rc = 20
# degrees_of_coverage = [2, 3, 4]
# GAMA_active_sensors = [40.7, 57, 72.9] 
# MASS_active_sensors = [33, 46, 63] 

# 100x100 300 sensors, rs = 15 rc = 30
# degrees_of_coverage = [2, 3, 4]
# GAMA_active_sensors = [81, 115, 147] 
# MASS_active_sensors = [58, 86, 108] 

# 150x150 500 sensors, rs = 20, rc = 40
degrees_of_coverage = [2, 3, 4]
GAMA_active_sensors = [125, 160, 211] 
MASS_active_sensors = [72, 110, 135] 

bar_width = 0.35

r1 = np.arange(len(degrees_of_coverage))
r2 = [x + bar_width for x in r1]

plt.figure(figsize=(10, 6))
plt.bar(r2, MASS_active_sensors, color='red', width=bar_width, edgecolor='grey', label='MASS')
plt.bar(r1, GAMA_active_sensors, color='navy', width=bar_width, edgecolor='grey', label='GAMA')

plt.xlabel('Degree of Coverage', fontweight='bold')
plt.ylabel('Number of Active Sensors', fontweight='bold')
plt.xticks([r + bar_width/2 for r in range(len(degrees_of_coverage))], degrees_of_coverage)

plt.title('Number of Active Sensors vs Degree of Coverage')
plt.legend()

plt.show()


# Points provided
# hundred_k4_points = [
#     (21, 6), (22, 16), (80, 80), (14, 36), (56, 27), (22, 81), (91, 27), (4, 21), (25, 38), (39, 87),
#     (11, 27), (55, 76), (65, 20), (93, 25), (55, 52), (37, 84), (82, 28), (31, 5), (66, 89), (32, 78),
#     (72, 40), (30, 26), (1, 56), (88, 98), (73, 8), (94, 79), (25, 55), (74, 67), (48, 3), (2, 13),
#     (99, 26), (27, 51), (100, 74), (90, 98), (69, 5), (70, 26), (75, 35), (99, 5), (3, 43), (91, 33),
#     (68, 57), (40, 35), (55, 54), (59, 83), (2, 66), (30, 63), (74, 51), (85, 77), (47, 33), (79, 2),
#     (18, 89), (95, 55), (91, 4), (45, 57), (7, 5), (87, 54), (96, 85), (94, 81), (80, 76), (94, 48),
#     (56, 73), (94, 61), (10, 66), (12, 6), (41, 67), (2, 64), (87, 96), (50, 9), (95, 46), (35, 28),
#     (61, 97), (99, 59), (41, 96), (63, 41), (54, 48), (5, 34), (47, 87), (14, 84), (2, 98), (4, 20),
#     (19, 13), (24, 95), (24, 86), (36, 41), (53, 8), (15, 58), (60, 79), (74, 6), (4, 95), (5, 78),
#     (73, 57), (58, 21), (81, 100), (18, 42), (36, 11), (93, 11), (32, 12), (3, 3), (4, 54), (29, 65),
#     (1, 91), (53, 99), (1, 93), (90, 10), (62, 88), (26, 93), (0, 42), (43, 4)
# ]
one50_k2_points = [ (137, 87), (8, 65), (133, 32), (32, 95), (67, 107),
    (145, 131), (0, 29), (130, 132), (11, 117), (28, 138),
    (60, 17), (108, 43), (26, 143), (126, 48), (62, 141),
    (101, 90), (60, 73), (44, 98), (145, 73), (52, 33),
    (92, 98), (44, 129), (79, 93), (127, 85), (56, 80),
    (140, 61), (75, 137), (145, 139), (55, 62), (45, 63),
    (69, 9), (61, 42), (81, 38), (42, 45), (109, 123),
    (113, 0), (97, 137), (132, 102), (93, 58), (119, 132),
    (120, 52), (12, 30), (2, 9), (37, 8), (78, 28),
    (33, 6), (132, 110), (121, 66), (108, 140), (104, 34),
    (23, 72), (35, 117), (84, 15), (77, 119), (15, 88),
    (119, 106), (78, 76), (140, 16), (1, 81), (118, 10),
    (106, 2), (1, 150), (7, 111), (142, 40), (24, 32),
    (9, 56), (55, 140), (98, 67), (133, 10), (11, 11),
    (6, 148), (89, 103)
]

one50_k4_points = [(10, 68), (45, 35), (135, 1), (56, 57), (83, 50), (93, 66), (74, 95), (10, 125),
    (117, 112), (107, 92), (9, 91), (141, 70), (36, 9), (119, 137), (70, 136), (122, 136),
    (44, 114), (98, 60), (101, 139), (65, 18), (118, 6), (115, 13), (77, 132), (81, 132),
    (142, 68), (36, 112), (140, 45), (8, 41), (99, 11), (125, 61), (147, 148), (8, 131),
    (5, 31), (102, 44), (22, 35), (42, 1), (146, 132), (80, 50), (34, 80), (20, 45),
    (45, 55), (47, 139), (34, 60), (147, 8), (60, 150), (79, 0), (9, 132), (48, 33),
    (8, 132), (133, 25), (11, 18), (7, 16), (49, 77), (113, 118), (7, 61), (10, 92),
    (23, 147), (110, 76), (101, 136), (59, 105), (81, 17), (36, 94), (79, 9), (2, 41),
    (145, 141), (96, 106), (150, 126), (100, 30), (11, 118), (142, 12), (17, 119), (136, 87),
    (145, 45), (69, 44), (136, 98), (75, 79), (18, 145), (29, 8), (100, 105), (29, 94),
    (15, 7), (4, 1), (44, 75), (69, 132), (55, 143), (134, 46), (2, 89), (22, 145),
    (85, 107), (108, 91), (38, 97), (74, 39), (77, 95), (20, 150), (95, 34), (136, 75),
    (83, 83), (65, 101), (129, 92), (52, 14), (139, 96), (75, 64), (40, 57), (60, 15),
    (85, 74), (60, 68), (3, 59), (116, 2), (7, 0), (137, 105), (147, 27), (132, 145),
    (101, 49), (39, 22), (128, 33), (82, 9), (104, 123), (126, 118), (9, 36), (132, 2),
    (46, 142), (52, 114), (33, 132), (37, 76), (146, 58), (46, 12), (138, 119), (4, 99),
    (110, 150), (123, 57), (110, 71), (124, 35), (45, 36), (2, 75), (95, 141)
]

Rs = 20

grid_size = 150
coverage_grid = np.zeros((grid_size, grid_size))

for x, y in one50_k4_points:
    for i in range(grid_size):
        for j in range(grid_size):
            if np.sqrt((x - i) ** 2 + (y - j) ** 2) <= Rs:
                coverage_grid[i, j] += 1

plt.plot()
plt.imshow(coverage_grid)
plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.show()
