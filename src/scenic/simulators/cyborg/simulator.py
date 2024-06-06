from typing import Any
from CybORG.Shared import Scenario
from CybORG.Simulator.SimulationController import SimulationController

from collections import defaultdict
from scenic.core.scenarios import Scene
from scenic.core.simulators import Simulation, Simulator
from scenic.simulators.cyborg.objects import CybORGSubnet, CybORGHost, CybORGAgent, CybORGEgoAgent
from . import CybORGObject

class CybORGSimulator(Simulator):
    def __init__(self):
        super().__init__()

    def createSimulation(self, scene, **kwargs):
        scenario = self._scene_to_scenario(scene)
        return CybORGSimulation(scene, SimulationController(scenario), **kwargs)

    def _initialize_subnet(self, subnet: CybORGSubnet):
        subnetData = {"Size": 0, "Hosts": []}
        # TODO NACLs
        # Also special handling for defender and attacker subnets, if this game uses them
        return subnetData

    def _scene_to_scenario(self, scene: Scene) -> Scenario:
        sc: dict[str, dict[str, Any]] = {"Agents": {}, "Subnets": {}, "Hosts": {"Defender": {"image": "Velociraptor_Server"}}}
        for obj in scene.objects:
            if isinstance(obj, CybORGSubnet) and obj.cyborg_name not in sc["Subnets"]:
                sc["Subnets"][obj.cyborg_name] = self._initialize_subnet(obj)
            elif isinstance(obj, CybORGHost):
                hostData = {"image": "Internal", "info": {obj.cyborg_name: "All"}}
                # TODO image, confidentiality, availability
                # could have subnet+image mapped to latter 2 per scenario
                # for instance, subnet of unimportant servers but users with confidential documents
                # vs a subnet of important servers and unimportant users
                # TODO info interfaces
                # info is a dict mapping hostnames to a level of info that red acquires on compromising a host
                # 'All' means red gets access to the host, while 'IP Address' just means that red becomes aware of the host without needing to scan
                # This is used for lateral movement, so for every subnet that the red agent does not start in
                # there should be at least one path back to the red agent's starting subnet following info links
                if obj.subnet.cyborg_name not in sc["Subnets"]:
                    sc["Subnets"][obj.subnet.cyborg_name] = self._initialize_subnet(obj.subnet)
                sc["Subnets"][obj.subnet.cyborg_name]["Size"] += 1
                sc["Subnets"][obj.subnet.cyborg_name]["Hosts"].apppend(obj.cyborg_name)
                sc["Hosts"][obj.cyborg_name] = hostData
            elif isinstance(obj, CybORGAgent):
                agentData = {"agent_type": "SleepAgent", "Actions": ["Sleep"], "wrappers": [], "starting_sessions": [], "reward_calculator_type": None, "INT": {"Hosts": {}}, "AllowedSubnets": []}
                # TODO agent type, allowed subnets, actions, reward calcuator, initial access
                if isinstance(obj, CybORGEgoAgent):
                    # First generate session for defender
                    agentData["starting_sessions"].append({"name": "VeloServer", "username": "ubuntu", "type": "VelociraptorServer", "hostname": "Defender", "artifacts": []})
                    # TODO artifacts
                    # Then generate sessions for all hosts
                    # We need a client for the defender unless the defender is in its own subnet, which doesn't have a flag yet
                    # TODO map image names to usernames so that we can be SYSTEM on Windows
                    # curiously we seem to use ubuntu on all linux systems instead of root
                    for host in sc["Hosts"]:
                        if host != "Attacker":
                            agentData["starting_sessions"].append({"name": "Velo_" + host, "username": "ubuntu", "type": "VelociraptorClient", "hostname": host, "parent": "VeloServer"})
                            agentData["INT"]["Hosts"][host] = {"User info": "All", "System info": "All", "Interfaces": "All"}
                    agentData["AllowedSubnets"] = list(sc["Subnets"].keys())
                    # TODO remove attacker subnet if present
                else:
                    # Turn session tuple into the real deal
                    agentData["starting_sessions"].append(obj.session._asdict())
                    # TODO this, or make a system for generating such
                    # May need to maintain a reverse subnet dict
                    # agentData["AllowedSubnets"].append(sc["Hosts"][obj.session.hostname])
                    agentData["INT"]["Hosts"][obj.session.hostname] = {"System info": "All", "Interfaces": "All"}

        return Scenario(sc)

class CybORGSimulation(Simulation):
    def __init__(self, scene, controller: SimulationController, **kwargs):
        self.mode2D = scene.compileOptions.mode2D
        self.usedObjectNames = defaultdict(lambda: 0)
        self.controller = controller
        self.actions = []
        super().__init__(scene, **kwargs)

    def setup(self):
        super().setup()
        self.controller.reset()

    def queue_action(self, agent, action):
        self.actions.append(action)

    def step(self):
        super().step()
        for v in self.actions:
            self.controller.execute_action(v)
        self.actions.clear()
        # TODO determine done? cyborg does not have a termination rule by default
        self.controller.step()

    def createObjectInSimulator(self, obj):
        pass
        # Don't think we actually need anything here
        # scene to scenario should handle object linking

    def getProperties(self, obj, properties):
        if not isinstance(obj, CybORGObject):
            return {prop: getattr(obj, prop) for prop in properties}

        # TODO: everything, especially position
        # Maybe borrow some code from David's visualizer? Should cache positions
        # Do we need to indicate regions for different subnets? Maybe only if they show up
