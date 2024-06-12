model scenic.simulators.cyborg.model

from scenic.simulators.cyborg import AgentType, RewardCalculator, BlueActions, ActionWrapper
from CybORG.Shared.Actions import Sleep

# since kind.size is an input to a range we can't even uniform the kind
# what fun
# i am having fun
for i, kind in enumerate((SubnetKind.USER, SubnetKind.ENTERPRISE, SubnetKind.OPER, SubnetKind.USER, SubnetKind.OPER)):
    genSubnet(kind)
    genHosts(i, kind.size)


genLinks()

behavior SleepBehaviour():
    while True:
        take ActionWrapper(Sleep)

_ego, green, defender, villain = genAgents(SleepBehaviour)
ego = _ego
