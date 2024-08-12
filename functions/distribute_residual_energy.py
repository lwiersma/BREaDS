import config

def distribute_residual_energy(df, residue, i):
    '''
    This function distributes renewable energy that has not been used for meeting the load profile directly. Priorities for distribution can be set up here.
    '''
    if df['State of charge battery [kWh]'][i] < config.battery_capacity:
        if ((config.battery_capacity - df['State of charge battery [kWh]'][i]) >= residue['Residual renewables profile [kW]'][i]) \
            and (residue['Residual renewables profile [kW]'][i] < config.charge_rate):
            df['Charge battery with renewables [kW]'][i] = residue['Residual renewables profile [kW]'][i]
        elif ((config.battery_capacity - df['State of charge battery [kWh]'][i]) >= residue['Residual renewables profile [kW]'][i]) \
            and (residue['Residual renewables profile [kW]'][i] >= config.charge_rate):
            df['Charge battery with renewables [kW]'][i] = config.charge_rate
            df['Export to grid [kW]'][i] = (df['Charge battery with renewables [kW]'][i] - config.charge_rate)
        elif ((config.battery_capacity - df['State of charge battery [kWh]'][i]) < residue['Residual renewables profile [kW]'][i]) \
            and (residue['Residual renewables profile [kW]'][i] < config.charge_rate):
            df['Charge battery with renewables [kW]'][i] = (config.battery_capacity - df['State of charge battery [kWh]'][i])
            df['Export to grid [kW]'][i] = (residue['Residual renewables profile [kW]'][i] \
                                            - (config.battery_capacity - df['State of charge battery [kWh]'][i]))       
        elif ((config.battery_capacity - df['State of charge battery [kWh]'][i]) < residue['Residual renewables profile [kW]'][i]) \
            and (residue['Residual renewables profile [kW]'][i] >= config.charge_rate):
            df['Charge battery with renewables [kW]'][i] = config.charge_rate
            df['Export to grid [kW]'][i] = (residue['Residual renewables profile [kW]'][i] - config.charge_rate)
    else:
        df['Export to grid [kW]'][i] = residue['Residual renewables profile [kW]'][i]

    if i < 8759:
        df['State of charge battery [kWh]'][i+1] += (df['State of charge battery [kWh]'][i] + df['Charge battery with renewables [kW]'][i])
    else:
        pass