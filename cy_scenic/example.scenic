model scenic.simulators.cyborg.model

from scenic.simulators.cyborg import AgentType, RewardCalculator, BlueActions, ActionWrapper
from CybORG.Shared.Actions import Sleep, Monitor, Remove, Restore

# Have to fix the number and kind of subnets since trying to randomize causes recursive random
subnets = (SubnetKind.USER, SubnetKind.ENTERPRISE, SubnetKind.OPER, SubnetKind.USER, SubnetKind.OPER)
image_map = {
    SubnetKind.USER: {
        Image.LINUX_USER_HOST1: (Confidentiality.NONE, Availability.LOW), Image.LINUX_USER_HOST2: (Confidentiality.NONE, Availability.LOW),
        Image.WINDOWS_USER_HOST1: (Confidentiality.LOW, Availability.LOW), Image.WINDOWS_USER_HOST2: (Confidentiality.LOW, Availability.LOW)
    },
    SubnetKind.OPER: {
        Image.GATEWAY: (Confidentiality.NONE, Availability.MED), Image.OP_SERVER: (Confidentiality.MED, Availability.MED)
    },
    SubnetKind.ENTERPRISE: {
        Image.GATEWAY: (Confidentiality.NONE, Availability.MED), Image.INTERNAL: (Confidentiality.HI, Availability.HI)
    }
}

for i, kind in enumerate(subnets):
    genSubnet(kind, image_map)
    # Different subnets
    genHosts(i, kind.size)

genRandomLinks()

behavior ReactBehaviour(agent: str, action: ActionWrapper):
    infected = set()
    while True:
        obs = simulation().get_agent_obs(agent)
        for k, v in obs.items():
            if not isinstance(v, dict):
                continue
            if any(map(lambda x: "PID" in x, host_info.get('Processes', []))) > 0:
                infected.add(k)
        # Blue sessions are always 0, and the agent parameter will be automatically added
        if infected:
            take ActionWrapper(action, session=0, hostname=infected.pop())
        else:
            take ActionWrapper(Monitor, session=0)
            # take SleepActionWrapper() # Sleep doesn't need arguments

# Green agent automatically gets Green behaviour
greenAgent = new GreenAgent
hostRed = Uniform(*filter(lambda x: x.image is not Image.GATEWAY and x.image in image_map[SubnetKind.USER].keys(), getHosts()))
red = new Agent above hostRed by 0.75, with name "Red", with agent_type AgentType.MEANDER,
    with session CybORGSession(hostRed, "RedAbstractSession", "RedPhish")

defenderSubnet = Uniform(*tuple(getSubnets()))
hostDefender = new Host with name "Defender", with image Image.VELOCIRAPTOR_SERVER, with subnet defenderSubnet,
    with confidentiality Confidentiality.HI, with availability Availability.NONE, above defenderSubnet
ego = new EgoAgent above hostDefender by 0, with behavior ReactBehaviour("Blue", Remove)
