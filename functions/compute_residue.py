import pandas as pd

import config

from functions.distribute_residual_energy import *
from functions.service_residual_load import *

def compute_residue(df):
    '''
    This function computes the residual demand, after a first iteration of meeting the load profile with the renewables profile.
    It also initialises all columns for looping through the dataframe and distributing energy.
    '''
    df['Load serviced by renewables [kW]'] = df[['Load profile [kW]', 'Renewables profile [kW]']].min(axis=1)
    df['Load serviced by battery [kW]'] = 0.0
    df['Load serviced by grid [kW]'] = 0.0

    df['State of charge battery [kWh]'] = config.initial_state
    df['Charge battery with renewables [kW]'] = 0.0
    df['Charge battery with grid [kW]'] = 0.0
    df['Export to grid [kW]'] = 0.0
    
    residue = pd.DataFrame()
    residue['Residual load profile [kW]'] = df['Load profile [kW]'] - df['Load serviced by renewables [kW]']
    residue['Residual renewables profile [kW]'] = df['Renewables profile [kW]'] - df['Load serviced by renewables [kW]']

    for i in range(len(df)):
        if residue['Residual load profile [kW]'][i] > 0.0:
            service_residual_load(df, residue, i)
        elif residue['Residual renewables profile [kW]'][i] > 0.0:
            distribute_residual_energy(df, residue, i)

    return df