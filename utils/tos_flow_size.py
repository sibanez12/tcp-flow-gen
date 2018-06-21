
import numpy as np

MIN_FLOW_SIZE = 1<<20     # 1MB
MAX_FLOW_SIZE = (1<<27)-1 # 4MB

tos_vals = [0x04, 0x08, 0x0C, 0x10, 0x20, 0x28, 0x30, 0x38, 0x40, 0x48, 0x50, 0x58, 0x60, 0x68, 0x70, 0x78, 0x80, 0x88, 0x90, 0x98, 0xA0, 0xB0, 0xB8, 0xC0, 0xE0]
flow_sizes = map(int, list(np.linspace(MIN_FLOW_SIZE, MAX_FLOW_SIZE, len(tos_vals))))

tos_size_map = {}
size_tos_map = {}

for tos, size in zip(tos_vals, flow_sizes):
    tos_size_map[tos] = size
    size_tos_map[size] = tos

