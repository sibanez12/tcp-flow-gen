#!/usr/bin/env python

import sys, os, argparse
from flow_generator import FlowGenerator

def gen_flows(workload):
    fg = FlowGenerator(workload)
    fg.runExperiment()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('workload', type=str, help="workload file that contains the flows to generate")
    args = parser.parse_args()

    gen_flows(args.workload)


if __name__ == "__main__":
    main()
