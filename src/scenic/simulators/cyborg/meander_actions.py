from scenic.core.dynamics import *


# base action class for Red Meander Agent
class RedAction(Action):
    def apply(self, environment, agent):
        raise NotImplementedError("Each action must define its application logic.")


class ScanSubnetAction(RedAction):
    """scans a specified subnet to discover active IPs"""
    def __init__(self, subnet):
        self.subnet = subnet

    def apply(self, environment, agent):
        print(f"Scanning subnet: {self.subnet}")
        return environment.scan_subnet(self.subnet, agent)


class ExploitHostAction(RedAction):
    """tries to exploit a vulnerable host found in the subnet"""
    def __init__(self, host_ip):
        self.host_ip = host_ip

    def apply(self, environment, agent):
        print(f"Exploiting host at IP: {self.host_ip}")
        return environment.exploit_host(self.host_ip, agent)
