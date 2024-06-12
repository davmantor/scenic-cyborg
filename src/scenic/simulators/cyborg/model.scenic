simulator CybORGSimulator

import itertools

from scenic.simulators.cyborg.objects import *
from scenic.simulators.cyborg.enums import Image, SubnetKind

# FIXME why is this clipping into hosts?
class Subnet(CybORGSubnet):
    width: 12
    length: 12
    height: 0.004
    allowCollisions: True
    shape: CylinderShape()
    color: (0.75, 0.75, 0.75)

class Host(CybORGHost):
    width: 0.75
    length: 0.75
    height: 1.5
    shape: BoxShape()
    color: (0.25, 0.25, 0.25)
    position: new Point on self.subnet.region
    # TODO precalc circle or something, reuse code from vbird if i can
    allowCollisions: True

class Agent(CybORGAgent):
    width: 0.5
    length: 0.5
    height: 0.004
    shape: CylinderShape()
    allowCollisions: True
    color: (1, 0, 0)
    positionStdDev: (0, 0, 0)

# we need a positive width, but we want this to be invisible...
# sadly scenic breaks if we manually construct an actually empty mesh
class GreenAgent(CybORGGreenAgent):
    width: 0.004
    length: 0.004
    height: 0.004
    allowCollisions: True
    color: (0, 1, 0)

class EgoAgent(CybORGEgoAgent):
    width: 0.5
    length: 0.5
    height: 0.004
    # I would like it to be above hostDefender all the time, which wouldn't need this to be True
    # But it seems that floating point error(?) can cause "above hostDefender by 0" to be a collision sometimes
    allowCollisions: True
    shape: CylinderShape()
    color: (0, 0, 1)
    positionStdDev: (0, 0, 0)

_subnets = []
# TODO write more or (better) make a generator
# assuming a radius of 4, leave a distance of 2 between each circle
_subnetPos = ((0, 0, 0), (-14, -14, 0), (-14, 14, 0), (14, 14, 0), (14, -14, 0))
def genSubnet(kind: SubnetKind):
    obj = new Subnet with name str(kind.name) + str(len(_subnets)),
            with region CircularRegion(_subnetPos[len(_subnets)], 6),
            with kind kind,
            at _subnetPos[len(_subnets)]
            # TODO image map, likely defined as part of kind
    _subnets.append((obj, []))
    return obj

_hosts = []
def genHost(ind: int):
    subnet, count = _subnets[ind]
    if subnet.kind.makeOne and not count:
        img = kind.makeOne
    else:
        img = Discrete(subnet.kind.images)
    # BUG if you don't convert every name to string manually it will try to generate some distribution
    # that calls str.__radd_ which doesn't exist but there's no fucking traceback so do it right every time
    # or tear your hair out i guess
    obj = new Host with name str(subnet.name) + str(len(count)),
            with subnet subnet,
            with image img
    _hosts.append(obj)
    count.append(obj)
    return obj

class Link(CybORGLink):
    allowCollisions: True
    shape: BoxShape()
    color: (0.75, 0, 0)
    width: 0.1
    height: 0.004

def genLinks():
    tolink = _subnets.copy()
    while len(tolink) > 1:
        p1 = tolink[-1]
        del tolink[-1]
        p2 = Uniform(*tuple(itertools.chain.from_iterable(map(lambda x: (x[1][0],) if x[0].kind.makeOne else x[1], tolink))))
        if p1[0].kind.makeOne:
            p1 = p1[1][0]
        else:
            p1 = Uniform(*tuple(p1[1]))
        new Link at p1 offset along angle from p1 to p2 by (0, (distance from p1 to p2) / 2, 0), facing directly toward p2, with p1 p1, with p2 p2, with length distance from p1 to p2

def genAgents(behave):
    greenAgent = new GreenAgent
    defenderSubnet = Uniform(*tuple(map(lambda x: x[0], _subnets)))
    hostDefender = new Host with name "Defender", with image Image.VELOCIRAPTOR_SERVER, with subnet defenderSubnet
    blueAgent = new EgoAgent above hostDefender by 0, with behavior behave
    return blueAgent, greenAgent, hostDefender
