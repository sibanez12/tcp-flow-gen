#!/usr/bin/env python

import sys, os, re, argparse
import numpy as np

from utils.tos_flow_size import tos_vals, tos_size_map

#### SRPT ####
#DST_IP = '10.1.1.1'
#SRC_IPs = ['10.1.1.2', '10.1.1.5']

#### FCFS ####
DST_IP = '10.1.1.5'
SRC_IPs = ['10.1.1.1', '10.1.1.2']

line_fmat = '{numBytes}: {srcIP}, {dstIP}\n'

def make_flow(tos, src):
    size = tos_size_map[tos]
    return line_fmat.format(**{'numBytes':size, 'srcIP':src, 'dstIP':DST_IP})

# 3 flows
def gen_workload(filename):
    with open(filename, 'w') as f:
        tos = tos_vals[-1]
        srcIP = SRC_IPs[0]
        f.write(make_flow(tos, srcIP))

        tos = tos_vals[len(tos_vals)/3]
        srcIP = SRC_IPs[1]
        f.write(make_flow(tos, srcIP))

        tos = tos_vals[0]
        srcIP = SRC_IPs[1]
        f.write(make_flow(tos, srcIP))

# 10 flows
def gen_workload(filename):
    with open(filename, 'w') as f:
        tos = tos_vals[-1]
        srcIP = SRC_IPs[0]
        f.write(make_flow(tos, srcIP))

        tos = tos_vals[len(tos_vals)/3]
        srcIP = SRC_IPs[1]
        f.write(make_flow(tos, srcIP))

        for i in range(8):
            tos = tos_vals[0]
            srcIP = SRC_IPs[i % 2]
            f.write(make_flow(tos, srcIP))



#def gen_workload(filename, numFlows):
#    with open(filename, 'w') as f:
#        for i in range(numFlows):
#            tos = tos_vals[(len(tos_vals) - 1 - i) % (len(tos_vals))]
#            #tos = tos_vals[9-i]
#            size = tos_size_map[tos]
#            src = SRC_IPs[i % len(SRC_IPs)]
#            f.write(line_fmat.format(**{'numBytes':size, 'srcIP':src, 'dstIP':DST_IP}))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help="name of the file to generate")
    parser.add_argument('--numFlows', type=int, required=False, help='number of flows to generate')
    args = parser.parse_args()

    gen_workload(args.filename)


if __name__ == "__main__":
    main()
