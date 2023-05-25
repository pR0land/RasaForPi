import genCrossCorrelation as gcc
import math
import numpy as np
import pyaudio

#constants determaning how much the maximum shift can be (from the speed of sound in m/sec and the distance between the
# mics in meters)
soundSpeed = 343.2
micDist = 0.08127
maxShiftSec = micDist / float(soundSpeed)

def getDoa(inputSignal, fs=1):
    # the amount of mics on the respeaker
    numberOfMics = 4
    # the amount of mic pairs on the speaker (diagonal pairs)
    numberOfMicPairs = int(numberOfMics/2)
    # the indexing of the mic groups (they are diagonal indexed)
    micGroups = [(0,2),(1,3)]
    # creats an array to hold the delays in each direction
    delayArray = [0]*numberOfMicPairs
    # creats an array to hold the angle computed from the delay in each direction
    angleFromDelayArray = [0]*numberOfMicPairs
    # variable to hold doa computed
    DOA = None
    for i, pair in enumerate(micGroups):
        #uses our generalized cross correlation to compute the delay in seconds using the inputsignal.
        #This is assuming that the input array consist of one sample from each mic concatenated
        delayArray[i] = gcc.genCrossCorrUsingPhaseTransform(inputSignal[pair[0]::4], inputSignal[pair[1]::4],fs=fs,maxShiftInSec=maxShiftSec)
        # computes the angle in degrees from the delay.
        angleFromDelayArray[i] = math.asin(delayArray[i]/maxShiftSec) * 180 / math.pi
    #takes the smallest angel as it is less susceptible to noice
    if np.abs(angleFromDelayArray[0]) < np.abs(angleFromDelayArray[1]):
        if angleFromDelayArray[1] > 0:
            DOA = (angleFromDelayArray[0] + 360) % 360
        else:
            DOA = (180 - angleFromDelayArray[0])
    else:
        if angleFromDelayArray[0] < 0:
            DOA = (angleFromDelayArray[1] + 360) % 360
        else:
            DOA = (180 - angleFromDelayArray[1])

        DOA = (DOA + 90 + 180) % 360

    DOA = ((-DOA + 135)+180) % 360

    return DOA
