from typing import Any, Optional
from collections import defaultdict, namedtuple

from CybORG.Simulator.Entity import Entity
from CybORG.Simulator.Host import Host
from CybORG.Simulator.SimulationController import SimulationController
from scenic.core.object_types import Object
from .enums import *

class CybORGObject(Object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cyborg_name = None

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        raise NotImplementedError()

    def get_properties(self, sim: SimulationController) -> dict[str, Any]:
        raise NotImplementedError()

class CybORGSubnet(CybORGObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # maps image names to pairs of default confidentiality and availability for that image
        # to use whatever cyborg's default is for that (or if the value will not be queried) map to None
        # (None, None) pairs can be omitted
        # this can be used to create a network of unimportant servers but impatient users/confidential document holders
        # and a network of important servers but unimportant workstations
        # or whatever combination you can think of
        self.image_map: dict[str, tuple[Availability]] = defaultdict(lambda: (Confidentiality.NONE, Availability.NONE))
        self.nacl: dict[str, tuple[bool]] = {}

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.state.subnets[sim.state.subnet_name_to_cidr[self.cyborg_name]]

class CybORGHost(CybORGObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subnet: CybORGSubnet = None
        self.image: str = None
        self.confidentiality: Optional[Confidentiality] = None
        self.availability: Optional[Availability] = None
        self.linked_hosts: list[str] = []

    def get_cyborg_obj(self, sim: SimulationController) -> Host:
        return sim.state.hosts[self.cyborg_name]

CybORGSession = namedtuple("CybORGSession", ("username", "hostname", "type", "name"))

# There's technically nothing stopping us from having other agents that have multiple host sessions
# but in practice only blue will use that feature
# Non-blue agents are not real/ego and only exist for scenario generation purposes
class CybORGAgent(CybORGObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session: Optional[CybORGSession] = None
        self.agent_type: AgentType = AgentType.SLEEP
        self.actions: list[RedActions | GreenActions | BlueActions] = [BlueActions.SLEEP]
        self.reward: RewardCalculator = RewardCalculator.NONE
        self.subnets: list[CybORGSubnet] = []
        # ???
        # self.allowCollisions = False

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.agent_interfaces[self.cyborg_name]

class CybORGGreenAgent(CybORGAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cyborg_name = "Green"
        self.agent_type = AgentType.GREEN
        self.actions = GreenActions._member_names_

class CybORGEgoAgent(CybORGAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cyborg_name = "Blue"
        self.artifacts: list[Artifacts] = []
