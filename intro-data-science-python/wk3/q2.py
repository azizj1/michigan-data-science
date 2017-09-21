import pandas as pd
import numpy as np
import q1

def answer():
    energy = q1.getEnergy()
    GDP = q1.getGdp()
    ScimEn = q1.getScimEn()
    print(energy.shape[0])
    print(GDP.shape[0])
    print(ScimEn.shape[0])
    originalLength = energy.shape[0] + GDP.shape[0] + ScimEn.shape[0]
    finalLength = q1.merge(energy, GDP ,ScimEn).shape[0]
    print(originalLength)
    print(finalLength)
    return originalLength - finalLength

print(answer())
