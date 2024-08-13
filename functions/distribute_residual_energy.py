import pandas as pd

import config

def distribute_residual_energy(df, 
                               residue, 
                               idx):
    '''
    This function distributes renewable energy thloc has not been used for meeting the load profile directly. Priorities for distribution can be set up here.
    '''
    if df['State of charge battery [kWh]'].loc[idx] < config.battery_capacity:
        if ((config.battery_capacity - df['State of charge battery [kWh]'].loc[idx]) >= residue['Residual renewables profile [kW]'].loc[idx]) \
            and (residue['Residual renewables profile [kW]'].loc[idx] < config.charge_rate):
            df.loc[idx, 'Charge battery with renewables [kW]'] = residue['Residual renewables profile [kW]'].loc[idx]
        elif ((config.battery_capacity - df['State of charge battery [kWh]'].loc[idx]) >= residue['Residual renewables profile [kW]'].loc[idx]) \
            and (residue['Residual renewables profile [kW]'].loc[idx] >= config.charge_rate):
            df.loc[idx, 'Charge battery with renewables [kW]'] = config.charge_rate
            df.loc[idx, 'Export to grid [kW]'] = (df['Charge battery with renewables [kW]'].loc[idx] - config.charge_rate)
        elif ((config.battery_capacity - df['State of charge battery [kWh]'].loc[idx]) < residue['Residual renewables profile [kW]'].loc[idx]) \
            and (residue['Residual renewables profile [kW]'].loc[idx] < config.charge_rate):
            df.loc[idx, 'Charge battery with renewables [kW]'] = (config.battery_capacity - df['State of charge battery [kWh]'].loc[idx])
            df.loc[idx, 'Export to grid [kW]'] = (residue['Residual renewables profile [kW]'].loc[idx] \
                                            - (config.battery_capacity - df['State of charge battery [kWh]'].loc[idx]))       
        elif ((config.battery_capacity - df['State of charge battery [kWh]'].loc[idx]) < residue['Residual renewables profile [kW]'].loc[idx]) \
            and (residue['Residual renewables profile [kW]'].loc[idx] >= config.charge_rate):
            df.loc[idx, 'Charge battery with renewables [kW]'] = config.charge_rate
            df.loc[idx, 'Export to grid [kW]'] = (residue['Residual renewables profile [kW]'].loc[idx] - config.charge_rate)
    else:
        df.loc[idx, 'Export to grid [kW]'] = residue['Residual renewables profile [kW]'].loc[idx]
    
    if idx != df.index[-1]:
        nh = idx + pd.Timedelta(hours=1)
        df.loc[nh, 'State of charge battery [kWh]'] += (df['State of charge battery [kWh]'].loc[idx] + df['Charge battery with renewables [kW]'].loc[idx]).astype(float)
    else:
        pass
    