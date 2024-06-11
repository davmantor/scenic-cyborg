import scenic
from scenic.simulators.cyborg import CybORGSimulator
scenario = scenic.scenarioFromFile('cy_scenic/example.scenic')
scene, _ = scenario.generate()
simulator = CybORGSimulator()
scenic.setDebuggingOptions(fullBacktrace=True)
simulation = simulator.simulate(scene, maxSteps=10)
if simulation:  # `simulate` can return None if simulation fails
    result = simulation.result
    for i, state in enumerate(result.trajectory):
            # print(f'Time step {i}: {state}')
            pass
