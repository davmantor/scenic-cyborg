from typing import Any
from CybORG.Shared import Scenario
from CybORG.Simulator.SimulationController import SimulationController

from collections import defaultdict
from scenic.core.scenarios import Scene
from scenic.core.simulators import Simulation, Simulator
from .enums import InitialAccessLevel
from scenic.simulators.cyborg.objects import CybORGSubnet, CybORGHost, CybORGAgent, CybORGEgoAgent, CybORGGreenAgent
from . import CybORGObject

class CybORGSimulator(Simulator):
    def __init__(self):
        super().__init__()

    def createSimulation(self, scene, **kwargs):
        scenario = self._scene_to_scenario(scene)
        return CybORGSimulation(scene, SimulationController(scenario), **kwargs)

    def _scene_to_scenario(self, scene: Scene) -> Scenario:
        sc: dict[str, dict[str, Any]] = {"Agents": {}, "Subnets": {}, "Hosts": {"Defender": {"image": "Velociraptor_Server"}}}
        # FIXME this should not depend on object order
        # also maybe calculate subnet size *after* everything gets added to it
        host_to_subnet: dict[str, str] = {}
        subnets: list[CybORGSubnet] = []
        hosts: list[CybORGHost] = []
        agents: list[CybORGAgent] = []
        for obj in scene.objects:
            if isinstance(obj, CybORGSubnet):
                subnets.append(obj)
            elif isinstance(obj, CybORGHost):
                hosts.append(obj)
            elif isinstance(obj, CybORGAgent):
                agents.append(obj)

        for obj in subnets:
            assert obj.cyborg_name not in sc["Subnets"]
            subnetData = {"Hosts": [], "NACLs": {}}
            # TODO Support port-specific NACLs? For now only all NACLs are supported for simplicity
            for k, v in obj.nacls:
                subnetData["NACLs"][k] = {"in": "all" if v[0] else "None", "out": "all" if v[1] else "None"}
            sc["Subnets"][obj.cyborg_name] = subnetData

        for obj in hosts:
            assert obj.cyborg_name not in sc["Hosts"]
            hostData = {"image": obj.image, "info": {obj.cyborg_name: {"Interfaces": "All"}}}
            if obj.confidentiality:
                hostData["Confidentiality"] = obj.confidentiality
            if obj.availability:
                hostData["Availability"] = obj.availability
            # info is a dict mapping hostnames to a level of info that red acquires on compromising a host
            # 'All' means red gets access to the host, while 'IP Address' just means that red becomes aware of the host without needing to scan
            # This is used for lateral movement, so for every subnet that the red agent does not start in
            # there should be at least one path back to the red agent's starting subnet following info links
            # I don't think we need more here, a super control host is highly unlikely
            for h in obj.linked_hosts:
                hostData["info"][h]["Interfaces"] = "IP Address"
            assert obj.subnet.cyborg_name in sc["Subnets"]
            sc["Subnets"][obj.subnet.cyborg_name]["Hosts"].apppend(obj.cyborg_name)
            sc["Hosts"][obj.cyborg_name] = hostData
            host_to_subnet[obj.cyborg_name] = obj.subnet.cyborg_name

        for obj in agents:
            # TODO double triple check that these are strings and not instances of the classes themselves
            assert obj.cyborg_name not in sc["Agents"]
            agentData = {"agent_type": obj.agent_type, "Actions": list(obj.actions), "wrappers": [], "starting_sessions": [],
                            "reward_calculator_type": obj.reward, "INT": {"Hosts": {}}, "AllowedSubnets": [x.cyborg_name for x in obj.subnets]}
            assert all(map(lambda x: x in sc["Subnets"].keys(), agentData["AllowedSubnets"]))
            assert "Sleep" in agentData["Actions"]
            # XXX initial access should probably be managed by specific subclasses? remove this once a decision is made
            # for k, v in obj.initial_access:
            #     if v == InitialAccessLevel.IP:
            #         agentData["INT"]["Hosts"][k] = {"Interfaces": "All"}
            #     elif v == InitialAccessLevel.ALL:
            #         agentData["INT"]["Hosts"][k] = {"Interfaces": "All", "System info": "All"}
            if isinstance(obj, CybORGEgoAgent):
                # First generate session for defender
                agentData["starting_sessions"].append({"name": "VeloServer", "username": "ubuntu", "type": "VelociraptorServer", "hostname": "Defender", "artifacts": obj.artifacts})
                # Then generate sessions for all hosts
                for host, d in sc["Hosts"]:
                    # We need a client session on the defender if it is part of the network
                    if host != "Attacker":
                        agentData["starting_sessions"].append({"name": "Velo_" + host, "username": "SYSTEM" if d["image"].lower().startswity("win") else "ubuntu", "type": "VelociraptorClient", "hostname": host, "parent": "VeloServer"})
                        agentData["INT"]["Hosts"][host] = {"User info": "All", "System info": "All", "Interfaces": "All"}
                agentData["AllowedSubnets"] = list(sc["Subnets"].keys())
            elif isinstance(obj, CybORGGreenAgent):
                for host, d in sc["Hosts"]:
                    if host != "Attacker" and host != "Defender":
                        if "enterprise" not in host.lower() and "server" not in host.lower():
                            agentData["starting_sessions"].append({"name": "Green_" + host, "username": "GreenAgent", "type": "green_session", "hostname": host})
                        agentData["INT"]["Hosts"][host] = {"User info": "All", "System info": "All", "Interfaces": "All"}
                agentData["AllowedSubnets"] = list(sc["Subnets"].keys())
            else:
                # Turn session tuple into the real deal
                agentData["starting_sessions"].append(obj.session._asdict())
                agentData["AllowedSubnets"].append(host_to_subnet[obj.session.hostname])
                agentData["INT"]["Hosts"][obj.session.hostname] = {"System info": "All", "Interfaces": "All"}

        for x in sc["Subnets"]:
            x["Size"] = len(x["Hosts"])

        return Scenario(sc)

class CybORGSimulation(Simulation):
    def __init__(self, scene, controller: SimulationController, steps: int = 500, **kwargs):
        self.mode2D = scene.compileOptions.mode2D
        self.usedObjectNames = defaultdict(lambda: 0)
        self.controller = controller
        self.actions = []
        self.steps = steps
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
        # how do we even signal up? unclear what class 'dynamic_scenario' is
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
