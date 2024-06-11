model scenic.simulators.cyborg.model

from scenic.simulators.cyborg import AgentType, RewardCalculator, BlueActions, ActionWrapper
from CybORG.Shared.Actions import Sleep

# since kind.size is an input to a range we can't even uniform the kind
# what fun
# i am having fun
for i in range(5):
    kind = SubnetKind.USER
    genSubnet(kind)
    for j in range(kind.size):
        genHost(i).name


genLinks()

behavior SleepBehaviour():
    while True:
        take ActionWrapper(Sleep)

_ego, green, defender = genAgents(SleepBehaviour)
ego = _ego
