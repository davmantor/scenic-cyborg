from typing import Any
from collections import namedtuple

from CybORG.Simulator.Entity import Entity
from CybORG.Simulator.Host import Host
from CybORG.Simulator.SimulationController import SimulationController
from scenic.core.object_types import Object

class CybORGObject(Object):
    def __init__(self, cyborg_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cyborg_name = cyborg_name

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        raise NotImplementedError()

    def get_properties(self, sim: SimulationController) -> dict[str, Any]:
        raise NotImplementedError()

class CybORGSubnet(CybORGObject):
    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.state.subnets[sim.state.subnet_name_to_cidr[self.cyborg_name]]

class CybORGHost(CybORGObject):
    def __init__(self, cyborg_name: str, subnet: CybORGSubnet, *args, **kwargs):
        super().__init__(self, cyborg_name, *args, **kwargs)
        self.subnet = subnet

    def get_cyborg_obj(self, sim: SimulationController) -> Host:
        return sim.state.hosts[self.cyborg_name]

CybORGSession = namedtuple("CybORGSession", ("username", "hostname", "type", "name"))

# Ideally this shouldn't be an object unless it's Ego
# But we need other agents to be part of the scene so that they can be converted into a Scenario
# There's technically nothing stopping us from having other agents that have multiple host sessions
# but in practice only blue will use that feature
class CybORGAgent(CybORGObject):
    def __init__(self, cyborg_name: str, session: CybORGSession, *args, **kwargs):
        super().__init__(cyborg_name, *args, allowCollisions = False, **kwargs)
        self.session = session

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.agent_interfaces[self.cyborg_name]

# TODO might be handy to either have a shortcut for making a green agent that can access all systems
# or a thing to make one green agent for each "user" host

class CybORGEgoAgent(CybORGAgent):
    def __init__(self, *args, **kwargs):
        super().__init__("Blue", None, *args, **kwargs)
