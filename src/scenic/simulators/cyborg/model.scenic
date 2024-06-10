simulator CybORGSimulator

from scenic.simulators.cyborg.objects import CybORGSubnet, CybORGHost, CybORGAgent, CybORGGreenAgent, CybORGEgoAgent

class Subnet(CybORGSubnet):
    width: 0
    length: 0
    height: 0
    allowCollisions: False
    shape: BoxShape()

class Host(CybORGHost):
    width: 0.75
    length: 0.75
    height: 1.5
    shape: BoxShape()
    color: [0.25, 0.25, 0.25]

class Agent(CybORGAgent):
    width: 0.5
    length: 0.5
    height: 0.004
    shape: CylinderShape()
    color: [1, 0, 0]

class GreenAgent(CybORGGreenAgent):
    width: 0.5
    length: 0.5
    height: 0.004
    shape: CylinderShape()
    color: [0, 1, 0]

class EgoAgent(CybORGEgoAgent):
    width: 0.5
    length: 0.5
    height: 0.004
    shape: CylinderShape()
    color: [0, 0, 1]
