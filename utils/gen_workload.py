#!/usr/bin/env python

import sys, os, re, argparse
import numpy as np

DST_IP = '10.0.0.1'
SRC_IPs = ['10.0.0.2']

line_fmat = '{numBytes}: {srcIP}, {dstIP}\n'

def gen_workload(filename, numFlows):
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str, help="name of the file to generate")
    parser.add_argument('--numFlows', type=int, required=True, help='number of flows to generate')
    args = parser.parse_args()

    gen_workload(args.filename, args.numFlows)


if __name__ == "__main__":
    main()
