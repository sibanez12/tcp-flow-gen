
import subprocess, shlex, math, sys, os, socket

from utils.workload import Workload
from get_ctime import *
from utils.ip_info import ip_info

LOG_DIR = 'logs/'

LOGGING_IFACES = [('han-2.stanford.edu', 'eth3'), ('han-3.stanford.edu', 'eth4'), ('han-5.stanford.edu', 'eth3')]
#LOGGING_IFACE = ('han-2.stanford.edu', 'eth3')

class FlowGenerator:

    """
    starts the rate monitor on each host
    starts iperf server on each destination machine
    """
    def __init__(self, workload):

        self.workload = workload        
        self.iperf_servers = []
        self.iperf_clients = []
        self.logging_processes = []

        self.startLogging() 

        for flow in workload.flows:
            self.setupFlow(flow)


    """
    Start capturing the logged packets
    """
    def startLogging(self):
        start_tcpdump = 'ssh root@{0} "tcpdump -i {1} -w /tmp/exp_log_{0}.pcap -B 1000000"'

        # start logging
        for (host, iface) in LOGGING_IFACES:
            p = self.startProcess(start_tcpdump.format(host, iface))
            self.logging_processes.append((host, p))

    """
    Start the iperf servers
    """
    def setupFlow(self, flow):
        start_iperf_server = 'ssh root@{0} "iperf3 -s -p {1}"' 

        # start iperf server on the destination
        p = self.startProcess(start_iperf_server.format(flow['dstHost'], flow['flowID']))
        self.iperf_servers.append((dstHost, p))

    """
    get the global start time, distributed to each of the
    required hosts, and run the experiment 
    """
    def runExperiment(self):
        start_iperf_client = os.path.expandvars('ssh root@{} "iperf3 -p {} -c {} -n {} --tos {}"')

        # start iperf clients on each src machine
        for flow in self.workload.flows:
            command = start_iperf_client.format(flow['srcHost'], flow['flowID'], flow['dstIP'], flow['numBytes'], flow['tos'])
            p = self.startProcess(command)
            self.iperf_clients.append((flow['srcHost'], p))

        # wait for all iperf clients to finish
        for (host, iperf_client) in self.iperf_clients:
            print "Waiting for iperf client on host {0} ...".format(host)
            iperf_client.wait()
            print "iperf client on host {0} finished with return code: {1}".format(host, iperf_client.returncode)

        self.cleanupExperiment()

    # kill all tcpdump logging processes
    # kill all iperf servers
    def cleanupExperiment(self):

        # kill all tcpdump logging processes
        for (host, log_process) in self.logging_processes:
            log_process.terminate() 
            command = 'ssh root@{0} "pkill -u root tcpdump"'.format(host) 
            rc = self.runCommand(command) 
            if rc not in [0,1]:
                print >> sys.stderr, "ERROR: {0} -- failed".format(command)

        # kill all iperf servers
        for (host, server) in self.iperf_servers:
            server.kill() 
            command = 'ssh root@{0} "pkill -u root iperf3"'.format(host)
            rc = self.runCommand(command) 
            if rc not in [0,1]:
                print >> sys.stderr, "ERROR: {0} -- failed".format(command)             

        # copy log files
        copy_log_file = 'scp root@{0}:/tmp/exp_log_{0}.pcap %s' % LOG_DIR
        os.system(os.path.expandvars('rm -rf {}'.format(LOG_DIR)))
        os.makedirs(log_dir)
        # copy the log file
        for (host, iface) in LOGGING_IFACES:
            self.runCommand(copy_log_file.format(host)) 

        # copy the workload file into the log directory
        os.system('cp {} {}'.format(self.workload.flowsFile, LOG_DIR))

    def runCommand(self, command):
        print "----------------------------------------"
        print "Running Command:\n"
        print "-->$ ", command
        print "----------------------------------------"
        return subprocess.call(command, shell=True)
    
    def startProcess(self, command):
        print "----------------------------------------"
        print "Starting Process:\n"
        print "-->$ ", command
        print "----------------------------------------"
        return subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

