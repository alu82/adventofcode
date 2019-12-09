import os
import itertools
from base.ShipComputer import ShipComputer

script_dir = os.path.dirname(__file__)
inputFile = open(script_dir + "/input", "r")

line = inputFile.readline()
input = line.split(",")

# Part 1
maxThrusterSignal=0
for phaseSettings in itertools.permutations([0,1,2,3,4]):
    inputSignal=0
    for i in range(5):
        phaseSetting=phaseSettings[i]
        computer = ShipComputer(input.copy(), [phaseSetting, inputSignal])
        computer.run()
        inputSignal = computer.getLastOutput()
    if inputSignal>maxThrusterSignal:
        maxThrusterSignal=inputSignal
print(maxThrusterSignal)

# Part 2
maxThrusterSignal=0
lastOutputE = 0
for phaseSettings in itertools.permutations([5,6,7,8,9]):
    computerA = ShipComputer(input.copy(), [phaseSettings[0]])
    computerB = ShipComputer(input.copy(), [phaseSettings[1]])
    computerC = ShipComputer(input.copy(), [phaseSettings[2]])
    computerD = ShipComputer(input.copy(), [phaseSettings[3]])
    computerE = ShipComputer(input.copy(), [phaseSettings[4]])
    computers = itertools.cycle([computerA, computerB, computerC, computerD, computerE])

    output = 0
    terminated = False
    while not terminated:
        currentComputer = next(computers)
        currentComputer.addArgument(output)
        currentComputer.run()
        output = currentComputer.getLastOutput()
        terminated = currentComputer.terminated

    maxThrusterSignal = computerE.getLastOutput() if computerE.getLastOutput()> maxThrusterSignal else maxThrusterSignal

print(maxThrusterSignal)