
import numpy as np

MIN_FLOW_SIZE = 1<<20     # bytes
MAX_FLOW_SIZE = (1<<32)-1 # bytes

tos_vals = [0x04, 0x08, 0x0C, 0x10, 0x20, 0x28, 0x30, 0x38, 0x40, 0x48, 0x50, 0x58, 0x60, 0x68, 0x70, 0x78, 0x80, 0x88, 0x90, 0x98, 0xA0, 0xB0, 0xB8, 0xC0, 0xE0]
flow_sizes = map(int, list(np.linspace(MIN_FLOW_SIZE, MAX_FLOW_SIZE, len(tos_vals))))
#  [1048576, 179961855, 358875135, 537788415, 716701695, 895614975, 1074528255, 1253441535, 1432354815, 1611268095, 1790181375, 1969094655, 2148007935, 2326921215, 2505834495, 2684747775, 2863661055, 3042574335, 3221487615, 3400400895, 3579314175, 3758227455, 3937140735, 4116054015, 4294967295]

tos_size_map = {}
size_tos_map = {}

for tos, size in zip(tos_vals, flow_sizes):
    tos_size_map[tos] = size
    size_tos_map[size] = tos

