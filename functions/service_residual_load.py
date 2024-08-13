import pandas as pd

import config

def service_residual_load(df, 
                          residue, 
                          idx):
    '''
    This function services energy for the residual load profile. Priorities for energy services can be set up here.
    '''
    if residue['Residual load profile [kW]'].loc[idx] <= df['State of charge battery [kWh]'].loc[idx]:
        if residue['Residual load profile [kW]'].loc[idx] <= config.discharge_rate:
            df.loc[idx, 'Load serviced by battery [kW]'] = residue['Residual load profile [kW]'].loc[idx]
        else:
            df.loc[idx, 'Load serviced by battery [kW]'] = config.discharge_rate
            df.loc[idx, 'Load serviced by grid [kW]'] = (residue['Residual load profile [kW]'].loc[idx] - config.discharge_rate)
    else:
        if residue['Residual load profile [kW]'].loc[idx] <= config.discharge_rate:
            df.loc[idx, 'Load serviced by battery [kW]'] = df['State of charge battery [kWh]'].loc[idx]
            df.loc[idx, 'Load serviced by grid [kW]'] = (residue['Residual load profile [kW]'].loc[idx] - df['State of charge battery [kWh]'].loc[idx])
        else:
            df.loc[idx, 'Load serviced by battery [kW]'] = config.discharge_rate
            df.loc[idx, 'Load serviced by grid [kW]'] = (residue['Residual load profile [kW]'].loc[idx] - config.discharge_rate)
    
    if idx != df.index[-1]:
        nh = idx + pd.Timedelta(hours=1)
        df.loc[nh, 'State of charge battery [kWh]'] += (df['State of charge battery [kWh]'].loc[idx] - df['Load serviced by battery [kW]'].loc[idx]).astype(float)
    else:
        pass