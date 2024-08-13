import pandas as pd

from dictionaries import battery_config

from functions import distribute_residual_energy
from functions import service_residual_load

def compute_residue(df):
    '''
    This function computes the residual demand, after a first iteration of meeting the load profile with the renewables profile.
    It also initialises all columns for looping through the dataframe and distributing energy.
    '''
    df = df.assign(
        **{
            'Load serviced by renewables [kW]': df[['Load profile [kW]',
                                                    'Renewables profile [kW]']].min(axis = 1),
            'Load serviced by battery [kW]': 0.0,
            'Load serviced by grid [kW]': 0.0,
            'State of charge battery [kWh]': battery_config['initial_state'],
            'Charge battery with renewables [kW]': 0.0,
            'Charge battery with grid [kW]': 0.0,
            'Export to grid [kW]': 0.0
        }
    )
    
    residue = pd.DataFrame().assign(
        **{
            'Residual load profile [kW]': df['Load profile [kW]'] - df['Load serviced by renewables [kW]'],
            'Residual renewables profile [kW]': df['Renewables profile [kW]'] - df['Load serviced by renewables [kW]']
        }
    )

    for idx in df.index:
        if residue.loc[idx, 
                       'Residual load profile [kW]'] > 0.0:
            service_residual_load(df, 
                                  residue, 
                                  idx)
        elif residue.loc[idx, 
                         'Residual renewables profile [kW]'] > 0.0:
            distribute_residual_energy(df, 
                                       residue, 
                                       idx)

    return df