simulator CybORGSimulator

from scenic.simulators.cyborg.objects import *
from scenic.simulators.cyborg.enums import Image, SubnetKind

# FIXME why is this clipping into hosts?
class Subnet(CybORGSubnet):
    width: 16
    length: 16
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
    # TODO apparently arranging a few hosts so they don't intersect is too fucking hard for scenic
    # i don't want to deal with this
    # probably precalc circle or something, reuse code from vbird if i can
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
# assuming a radius of 3, leave a distance of 2 between each circle
_subnetPos = ((0, 0, 0), (-18, -18, 0), (-18, 18, 0), (18, 18, 0), (18, -18, 0))
def genSubnet(kind: SubnetKind):
    obj = new Subnet with name str(kind.name) + str(len(_subnets)),
            with region CircularRegion(_subnetPos[len(_subnets)], 3),
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
    length: 1 # abs(self.p1.position.distanceTo(self.p1.position))

# FIXME well this is fucking broken alright
# remove the crap i wrote before the return later
def genLinks():
    for i, p1 in enumerate(_subnets):
        if i == len(_subnets) - 1:
            break
        p2 = _subnets[i + 1]
        if True or p1[0].kind.makeOne:
            p1 = p1[1][0]
        else:
            p1 = Uniform(*tuple(p1[1]))
            pass
        if True or p2[0].kind.makeOne:
            p2 = p2[1][0]
        else:
            pass
            p2 = Uniform(*tuple(p2[1]))
        new Link at p1, facing directly toward p2, with p1 p1, with p2 p2
    return
    # tolink = set(range(len(_subnets)))
    # while len(tolink) > 1:
    #     # Will using this here blow up generation?
    #     p1 = Uniform(tolink)
    #     tolink.remove(p1)
    #     p2 = Uniform(tolink)
    #     if _subnets[p1][0].kind.makeOne:
    #         p1 = _subnets[p1][1][0]
    #     else:
    #         p1 = Uniform(*tuple(_subnets[p1][1]))
    #     if _subnets[p2][0].kind.makeOne:
    #         p2 = _subnets[p2][1][0]
    #     else:
    #         p2 = Uniform(*tuple(_subnets[p2][1]))
    #     new Link at p1, facing directly toward p2

def genAgents(behave):
    greenAgent = new GreenAgent
    defenderSubnet = Uniform(*tuple(map(lambda x: x[0], _subnets)))
    hostDefender = new Host with name "Defender", with image Image.VELOCIRAPTOR_SERVER, with subnet defenderSubnet
    blueAgent = new EgoAgent above hostDefender by 0, with behavior behave
    return blueAgent, greenAgent, hostDefender
