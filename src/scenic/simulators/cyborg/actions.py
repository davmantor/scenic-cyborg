# Problem: this version of CybORG has a lot of actions for any possible scenario
# However, they can generally be broken into categories: defensive vs offensive, local vs remote, scanning vs exploiting, etc.
# With enough categorization we can hopefully create wrappers that can wrap (almost) anything

# While it is unlikely that this is possible due to complexity and time constraints
# I would like to try to create some kind of system to generate random action sets
# This is probably not as useful as a random network layout, but it would be interesting to play a game with, say, no ssh exploit
# Of course, the blue agent wouldn't know that the red agent is crippled in this way and might end up chasing false alarms

# I'm going to assume that green agents will *not* be handled by Scenic.
# We could randomize action probabilities, but randomizing red agent state transitions takes priority

from typing import Type
from scenic.core.simulators import Action
from CybORG.Shared.Actions import Action as CyAction
from .simulator import CybORGSimulation

# While there is some variance in how actions are constructed, especially those not used in CAGE
# the set of basic abstract actions (plus a few specific red ones) seem be be faily consistent
# Almost all actions take an agent and session to start, which should be managed by our interface
# Afterwards, it's a matter of specific args like hosts, which should be generated
# It can become a bit tricky if there are args with large domains like strings, though, such as with GetUserInfo (which is used in Scenario1)

# Or we can just cheap out and do something small like this and write utility wrappers for certain things as they become useful
# Should probably make one for Session...

class SleepActionWrapper(Action):
    # Sleep doesn't actually do anything, so we don't even need to run it
    def applyTo(self, agent, simulation):
        pass

class ActionWrapper(Action):
    def __init__(self, cls: Type[CyAction], **kwargs):
        self.action_cls = cls
        self.action_args = kwargs

    def applyTo(self, agent, simulation: CybORGSimulation):
        # FIXME scenic agents may be separate from our objects? docs are not clear
        self.action_args["agent"] = agent.cyborg_name
        simulation.queue_action(self.action_cls(**self.action_args))
