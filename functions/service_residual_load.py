import pandas as pd

import config

def service_residual_load(df, residue, i):
    '''
    This function services energy for the residual load profile. Priorities for energy services can be set up here.
    '''
    if residue['Residual load profile [kW]'][i] <= df['State of charge battery [kWh]'][i]:
        if residue['Residual load profile [kW]'][i] <= config.discharge_rate:
            df['Load serviced by battery [kW]'][i] = residue['Residual load profile [kW]'][i]
        else:
            df['Load serviced by battery [kW]'][i] = config.discharge_rate
            df['Load serviced by grid [kW]'][i] = (residue['Residual load profile [kW]'][i] - config.discharge_rate)
    else:
        if residue['Residual load profile [kW]'][i] <= config.discharge_rate:
            df['Load serviced by battery [kW]'][i] = df['State of charge battery [kWh]'][i]
            df['Load serviced by grid [kW]'][i] = (residue['Residual load profile [kW]'][i] - df['State of charge battery [kWh]'][i])
        else:
            df['Load serviced by battery [kW]'][i] = config.discharge_rate
            df['Load serviced by grid [kW]'][i] = (residue['Residual load profile [kW]'][i] - config.discharge_rate)
    
    if i < 8759:
        df['State of charge battery [kWh]'][i+1] += (df['State of charge battery [kWh]'][i] - df['Load serviced by battery [kW]'][i])
    else:
        pass
    