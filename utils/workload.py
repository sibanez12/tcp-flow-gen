

import sys, os, re
from ip_info import ip_info
from tos_flow_size import size_tos_map

class Workload:
    """
    This parses the input flows.txt file into a Workload
    object that is used by other parts of the infrastructure
    to setup and run the experiments
    """
    
    def __init__(self, flowsFile):
        self.flowsFile = flowsFile
        self.flowFormat = r'(?P<numBytes>[ \d]*): (?P<srcIP>[\d\.]*),[ ]*(?P<dstIP>[\d\.]*)'
        self.ip_info = ip_info 
        
        self.flows = []
        self.numFlows = None
        self.srcs = None
        self.dsts = None
        self.allIPs = None
        self.allHosts = None
        self.srcHosts = None
        self.dstHosts = None
    
        # parse the flowsFile
        with open(flowsFile) as f:
            doc = f.read()

            #  set self.flows        
            searchObj = re.search(self.flowFormat, doc)
            while searchObj is not None:
                self.flows.append(searchObj.groupdict())
                doc = doc[:searchObj.start()] + doc[searchObj.end():]
                searchObj = re.search(self.flowFormat, doc)

        self.srcs = [flow['srcIP'] for flow in self.flows]
        self.dsts = [flow['dstIP'] for flow in self.flows]
        self.allIPs = self.srcs + list(set(self.dsts) - set(self.srcs))
        self.allHosts = list(set([self.ip_info[IP]['hostname'] for IP in self.allIPs]))
        self.srcHosts = list(set([self.ip_info[IP]['hostname'] for IP in self.srcs]))
        self.dstHosts = list(set([self.ip_info[IP]['hostname'] for IP in self.dsts]))
        self.numFlows = len(self.flows)
        flow_id = 1
        for i, flow in zip(range(len(self.flows)), self.flows):
            flow['srcHost'] = self.ip_info[flow['srcIP']]['hostname']
            flow['dstHost'] = self.ip_info[flow['dstIP']]['hostname']
            size = int(flow['numBytes'])
            flow['numBytes'] = size
            flow['tos'] = size_tos_map[size]
            flow['flowID'] = flow_id
            flow_id += 1
            

