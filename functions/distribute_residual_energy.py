import pandas as pd

from dictionaries.battery_config import *

def distribute_residual_energy(df, 
                               residue, 
                               idx):
    '''
    This function distributes renewable energy that has not been used for meeting the load profile directly. Priorities for distribution can be set up here.
    '''
    if df.loc[idx, 'State of charge battery [kWh]'] < battery_config['battery_capacity']:
        if ((battery_config['battery_capacity'] - df.loc[idx, 'State of charge battery [kWh]']) >= residue.loc[idx, 'Residual renewables profile [kW]']) \
            and (residue.loc[idx, 'Residual renewables profile [kW]'] < battery_config['charge_rate']):
            df.loc[idx, 'Charge battery with renewables [kW]'] = residue.loc[idx, 'Residual renewables profile [kW]']
        elif ((battery_config['battery_capacity'] - df.loc[idx, 'State of charge battery [kWh]']) >= residue.loc[idx, 'Residual renewables profile [kW]']) \
            and (residue.loc[idx, 'Residual renewables profile [kW]'] >= battery_config['charge_rate']):
            df.loc[idx, 'Charge battery with renewables [kW]'] = battery_config['charge_rate']
            df.loc[idx, 'Export to grid [kW]'] = (df.loc[idx, 'Charge battery with renewables [kW]'] - battery_config['charge_rate'])
        elif ((battery_config['battery_capacity'] - df.loc[idx, 'State of charge battery [kWh]']) < residue.loc[idx, 'Residual renewables profile [kW]']) \
            and (residue.loc[idx, 'Residual renewables profile [kW]'] < battery_config['charge_rate']):
            df.loc[idx, 'Charge battery with renewables [kW]'] = (battery_config['battery_capacity'] - df.loc[idx, 'State of charge battery [kWh]'])
            df.loc[idx, 'Export to grid [kW]'] = (residue.loc[idx, 'Residual renewables profile [kW]'] \
                                            - (battery_config['battery_capacity'] - df.loc[idx, 'State of charge battery [kWh]']))       
        elif ((battery_config['battery_capacity'] - df.loc[idx, 'State of charge battery [kWh]']) < residue.loc[idx, 'Residual renewables profile [kW]']) \
            and (residue.loc[idx, 'Residual renewables profile [kW]'] >= battery_config['charge_rate']):
            df.loc[idx, 'Charge battery with renewables [kW]'] = battery_config['charge_rate']
            df.loc[idx, 'Export to grid [kW]'] = (residue.loc[idx, 'Residual renewables profile [kW]'] - battery_config['charge_rate'])
    else:
        df.loc[idx, 'Export to grid [kW]'] = residue.loc[idx, 'Residual renewables profile [kW]']
    
    if idx != df.index[-1]:
        nh = idx + pd.Timedelta(hours = 1)
        df.loc[nh, 'State of charge battery [kWh]'] += (df.loc[idx, 'State of charge battery [kWh]'] + df.loc[idx, 'Charge battery with renewables [kW]'])
    else:
        pass
    