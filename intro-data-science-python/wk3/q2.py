import pandas as pd
import q1

def answer():
    energy = q1.getEnergy()
    GDP = q1.getGdp()
    ScimEn = q1.getScimEn()
    energyGdp = pd.merge(energy, GDP, how='inner', left_on='Country', right_on='Country Name')
    energyScim = pd.merge(energy, ScimEn, how='inner', left_on='Country', right_on='Country')
    gdpScim = pd.merge(GDP, ScimEn, how='inner', left_on='Country Name', right_on='Country')
    energyGdpScim = q1.merge(energy, GDP, ScimEn)
    print('energy {}'.format(energy.shape[0]))
    print('gdp {}'.format(GDP.shape[0]))
    print('ScimEn {}'.format(ScimEn.shape[0]))
    print('energy+gdp {}'.format(energyGdp.shape[0]))
    print('energy+scim {}'.format(energyScim.shape[0]))
    print('gdp+scim {}'.format(gdpScim.shape[0]))
    print('energy+gdp+scim {}'.format(energyGdpScim.shape[0]))

    # in order to not double count, subtract off the differences
    return energy.shape[0] + GDP.shape[0] + ScimEn.shape[0] \
           - energyGdp.shape[0] - energyScim.shape[0] - gdpScim.shape[0]
print(answer())
