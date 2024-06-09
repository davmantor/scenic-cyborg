from typing import Any
from collections import defaultdict, namedtuple

from CybORG.Simulator.Entity import Entity
from CybORG.Simulator.Host import Host
from CybORG.Simulator.SimulationController import SimulationController
from scenic.core.object_types import Object
from .enums import *

class CybORGObject(Object):
    def __init__(self, cyborg_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cyborg_name = cyborg_name

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        raise NotImplementedError()

    def get_properties(self, sim: SimulationController) -> dict[str, Any]:
        raise NotImplementedError()

# why is this not a damn enum
# i could say that about a lot of cyborg really
class CybORGSubnet(CybORGObject):
    def __init__(self, cyborg_name: str, nacl: dict[str, tuple[bool]], image_map: dict[str, tuple[str]] = defaultdict(lambda: (None, None)), *args, **kwargs):
        super().__init__(cyborg_name, *args, **kwargs)
        # maps image names to pairs of default confidentiality and availability for that image
        # to use whatever cyborg's default is for that (or if the value will not be queried) map to None
        # (None, None) pairs can be omitted
        # this can be used to create a network of unimportant servers but impatient users/confidential document holders
        # and a network of important servers but unimportant workstations
        # or whatever combination you can think of
        if not isinstance(image_map, defaultdict):
            image_map = defaultdict(lambda: (None, None), image_map)
        self.image_map = image_map
        self.nacl = nacl

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.state.subnets[sim.state.subnet_name_to_cidr[self.cyborg_name]]

class CybORGHost(CybORGObject):
    def __init__(self, cyborg_name: str, subnet: CybORGSubnet, image: str, confidentiality: str = None, availability: str = None, linked_hosts: list[str] = [], *args, **kwargs):
        super().__init__(self, cyborg_name, *args, **kwargs)
        self.subnet = subnet
        self.image = image
        self.confidentiality = confidentiality or subnet.image_map[image][0]
        self.availability = availability or subnet.image_map[image][1]
        self.linked_hosts = linked_hosts

    def get_cyborg_obj(self, sim: SimulationController) -> Host:
        return sim.state.hosts[self.cyborg_name]

CybORGSession = namedtuple("CybORGSession", ("username", "hostname", "type", "name"))

# Ideally this shouldn't be an object unless it's Ego
# But we need other agents to be part of the scene so that they can be converted into a Scenario
# There's technically nothing stopping us from having other agents that have multiple host sessions
# but in practice only blue will use that feature
class CybORGAgent(CybORGObject):
    def __init__(self, cyborg_name: str, session: CybORGSession, agent_type: AgentType, reward: RewardCalculator, # initial_access: dict[CybORGHost, InitialAccessLevel],
            subnets: list[CybORGSubnet], actions: list[RedActions | GreenActions | BlueActions], *args, **kwargs):
        super().__init__(cyborg_name, *args, allowCollisions = False, **kwargs)
        self.session = session
        self.agent_type = agent_type
        self.actions = actions
        self.reward = reward
        self.subnets = subnets
        # self.initial_access = initial_access

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.agent_interfaces[self.cyborg_name]

class CybORGGreenAgent(CybORGAgent):
    def __init__(self, *args, **kwargs):
        super().__init__("Green", None, AgentType.GREEN_AGENT, RewardCalculator.NONE, *args, subnets=None, actions=GreenActions._member_names_, **kwargs)

class CybORGEgoAgent(CybORGAgent):
    def __init__(self, artifacts: list[Artifacts] = [], *args, **kwargs):
        super().__init__("Blue", None, *args, subnets = None, **kwargs)
        self.artifacts = artifacts
