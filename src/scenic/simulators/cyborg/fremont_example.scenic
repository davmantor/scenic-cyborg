class CybORGAgent:
   allowCollisions: True
   param1: 0
   param2: 0

behavior RedTeamBehavior():
    while True:
        take Uniform(Action1(), Action2())  # choose a random action each time step

behavior RLBehavior():
    while True:
        actions = runRLPolicy()
        take actions

red1 = new CybORGAgent with param1 42, with behavior RedTeamBehavior
red2 = new CybORGAgent with param1 0, with behavior RedTeamBehavior

blue = new CybORGAgent with behavior RLBehavior