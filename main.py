import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "network.sumocfg"]

import traci
import traci.constants as tc
import sumolib

class StatePublisher(traci.StepListener):
    def step(self, t=0):
        # receive vehicle data
        veh0 = traci.vehicle.getSubscriptionResults("veh0")
        veh1 = traci.vehicle.getSubscriptionResults("veh1")
        veh2 = traci.vehicle.getSubscriptionResults("veh2")
        # print vehicle data
        print("green %.2f m/s" % veh0[tc.VAR_SPEED])
        print("blue  %.2f m/s" % veh1[tc.VAR_SPEED])
        print("red   %.2f m/s" % veh2[tc.VAR_SPEED])
        # indicate that the step listener should stay active in the next step
        return True

print("Starting the TraCI server...\n")
traci.start(sumoCmd) 

print("Subscribing to vehicle data...\n")
traci.vehicle.subscribe("veh0", (tc.VAR_SPEED, tc.VAR_ACCEL, tc.VAR_POSITION, tc.VAR_LANE_ID))
traci.vehicle.subscribe("veh1", (tc.VAR_SPEED, tc.VAR_ACCEL, tc.VAR_POSITION, tc.VAR_LANE_ID))
traci.vehicle.subscribe("veh2", (tc.VAR_SPEED, tc.VAR_ACCEL, tc.VAR_POSITION, tc.VAR_LANE_ID))

print("Constructing a StatePublisher...")
statePub = StatePublisher()
traci.addStepListener(statePub)

step = 0
while step < 40:
    # advance the simulation
    print("\nsimulation step: %i" % step)
    traci.simulationStep()
    step += 1

print("Stopping the TraCI server...")
traci.close()