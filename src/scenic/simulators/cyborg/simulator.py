import asyncio
import time

import numpy as np

from scenic.core.simulators import (
    Simulation,
    SimulationCreationError,
    Simulator,
    SimulatorInterfaceWarning,
)
from scenic.core.type_support import toVector
from scenic.core.vectors import Orientation, Vector
from scenic.syntax.veneer import verbosePrint

# Import CybORG-specific modules
from CybORG import CybORG
from CybORG.Agents.Wrappers import FixedFlatWrapper

# Constants
AGENT_NAME = "BlueAgent"


class CybORGSimulator(Simulator):
    def __init__(self, scenario_file, timestep=1):
        # Initialize CybORG environment
        self.cyborg = CybORG(scenario_file, 'sim')
        self.env = FixedFlatWrapper(self.cyborg)
        self.timestep = timestep

        verbosePrint(
            "\n\nAll Available Actions:\n",
            self.env.get_action_space(AGENT_NAME),
            level=2,
        )

        super().__init__()

    def createSimulation(self, scene, **kwargs):
        return CybORGSimulation(self, scene, **kwargs)

    def destroy(self):
        super().destroy()


class CybORGSimulation(Simulation):
    def __init__(self, simulator, scene, **kwargs):
        self.simulator = simulator
        self.env = simulator.env
        self.agent_name = AGENT_NAME
        self.current_step = 0

        super().__init__(scene, **kwargs)

    def setup(self):
        # Reset the environment
        self.env.reset(agent=self.agent_name)
        super().setup()

    def createObjectInSimulator(self, obj):
        # Add logic to handle creation of objects/agents in CybORG
        if obj.blueprint == "Agent":
            obj.realObjName = obj.name
            # Additional setup for the agent if needed
        else:
            raise RuntimeError("Unsupported object blueprint: ", obj.blueprint)

    def step(self):
        # Perform an action and advance the simulation
        action = self.scene.getActionForAgent(self.agent_name)
        observation, reward, done, info = self.env.step(agent=self.agent_name, action=action)
        self.current_step += 1
        return observation, reward, done, info

    def destroy(self):
        # Clean up the environment
        self.env.reset(agent=self.agent_name)
        super().destroy()
        print("CybORG simulation destroyed")

    def getProperties(self, obj, properties):
        if obj.blueprint == "Agent":
            # Retrieve agent properties from the environment
            state = self.env.get_observation(self.agent_name)
            values = {
                'position': state['position'],
                'velocity': state['velocity'],
                'health': state['health'],
                # Add more properties as needed
            }
            return values
        else:
            raise RuntimeError("Unsupported object blueprint: ", obj.blueprint)
