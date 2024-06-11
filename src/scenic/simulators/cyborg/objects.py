from typing import Any, Optional
from collections import defaultdict, namedtuple

from trimesh import Trimesh

from CybORG.Simulator.Entity import Entity
from CybORG.Simulator.Host import Host
from CybORG.Simulator.SimulationController import SimulationController
from scenic.core.object_types import Object
from scenic.core.regions import Region
from .enums import *

class CybORGObject(Object):
    def __init__(self, properties, *args, **kwargs):
        assert "name" in properties
        super().__init__(properties, *args, **kwargs)

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        raise NotImplementedError()

    def get_properties(self, sim: SimulationController) -> dict[str, Any]:
        raise NotImplementedError()

class CybORGSubnet(CybORGObject):
    def __init__(self, properties, *args, **kwargs):
        # maps image names to pairs of default confidentiality and availability for that image
        # to use whatever cyborg's default is for that (or if the value will not be queried) map to None
        # (None, None) pairs can be omitted
        # this can be used to create a network of unimportant servers but impatient users/confidential document holders
        # and a network of important servers but unimportant workstations
        # or whatever combination you can think of
        assert "region" in properties
        # "kind" is not used by CybORG, so not required
        # only useful for our generation scripts
        if "image_map" not in properties:
            properties["image_map"] = defaultdict(lambda: (Confidentiality.NONE, Availability.NONE))
        if "nacl" not in properties:
            properties["nacl"] = {}
        super().__init__(properties, *args, **kwargs)

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.state.subnets[sim.state.subnet_name_to_cidr[self.name]]

class CybORGHost(CybORGObject):
    def __init__(self, properties, *args, **kwargs):
        assert "subnet" in properties
        assert "image" in properties
        if "confidentiality" not in properties:
            properties["confidentiality"] = None
        if "availability" not in properties:
            properties["availability"] = None
        super().__init__(properties, *args, **kwargs)

    def get_cyborg_obj(self, sim: SimulationController) -> Host:
        return sim.state.hosts[self.cyborg_name]

CybORGSession = namedtuple("CybORGSession", ("username", "hostname", "type", "name"))

# There's technically nothing stopping us from having other agents that have multiple host sessions
# but in practice only blue will use that feature
# Non-blue agents are not real/ego and only exist for scenario generation purposes
class CybORGAgent(CybORGObject):
    def __init__(self, properties, *args, **kwargs):
        if "session" not in properties:
            properties["session"] = None
        if "agent_type" not in properties:
            properties["agent_type"] = AgentType.SLEEP
        if "actions" not in properties:
            properties["actions"] = [BlueActions.SLEEP]
        if "reward" not in properties:
            properties["reward"] = RewardCalculator.NONE
        if "subnets" not in properties:
            properties["subnets"] = []
        super().__init__(properties, *args, **kwargs)

    def get_cyborg_obj(self, sim: SimulationController) -> Entity:
        return sim.agent_interfaces[self.name]

class CybORGGreenAgent(CybORGAgent):
    def __init__(self, properties, *args, **kwargs):
        if "name" not in properties:
            properties["name"] = "Green"
        properties["agent_type"] = AgentType.GREEN
        properties["actions"] = GreenActions._member_map_.values()
        super().__init__(properties, *args, **kwargs)

    def __setattr__(self, name, value):
        if name == "allowCollisions" and value:
            raise KeyboardInterrupt()
        return super().__setattr__(name, value)

class CybORGEgoAgent(CybORGAgent):
    def __init__(self, properties, *args, **kwargs):
        if "name" not in properties:
            properties["name"] = "Blue"
        if "artifacts" not in properties:
            properties["artifacts"] = []
        super().__init__(properties, *args, **kwargs)

# TODO this should be a line from p1's position to p2's position
class CybORGLink(Object):
    def __init__(self, properties, *args, **kwargs):
        assert "p1" in properties
        assert "p2" in properties
        super().__init__(properties, *args, **kwargs)
