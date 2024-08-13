import pandas as pd

from dictionaries.battery_config import *

def service_residual_load(df, 
                          residue, 
                          idx):
    '''
    This function services energy for the residual load profile. Priorities for energy services can be set up here.
    '''
    if residue.loc[idx, 'Residual load profile [kW]'] <= df.loc[idx, 'State of charge battery [kWh]']:
        if residue.loc[idx, 'Residual load profile [kW]'] <= battery_config['discharge_rate']:
            df.loc[idx, 'Load serviced by battery [kW]'] = residue.loc[idx, 'Residual load profile [kW]']
        else:
            df.loc[idx, 'Load serviced by battery [kW]'] = battery_config['discharge_rate']
            df.loc[idx, 'Load serviced by grid [kW]'] = (residue.loc[idx, 'Residual load profile [kW]'] - battery_config['discharge_rate'])
    else:
        if residue.loc[idx, 'Residual load profile [kW]'] <= battery_config['discharge_rate']:
            df.loc[idx, 'Load serviced by battery [kW]'] = df.loc[idx, 'State of charge battery [kWh]']
            df.loc[idx, 'Load serviced by grid [kW]'] = (residue.loc[idx, 'Residual load profile [kW]'] - df.loc[idx, 'State of charge battery [kWh]'])
        else:
            df.loc[idx, 'Load serviced by battery [kW]'] = battery_config['discharge_rate']
            df.loc[idx, 'Load serviced by grid [kW]'] = (residue.loc[idx, 'Residual load profile [kW]'] - battery_config['discharge_rate'])
    
    if idx != df.index[-1]:
        nh = idx + pd.Timedelta(hours = 1)
        df.loc[nh, 'State of charge battery [kWh]'] += (df.loc[idx, 'State of charge battery [kWh]'] - df.loc[idx, 'Load serviced by battery [kW]'])
    else:
        pass