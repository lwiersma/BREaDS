'''
This dictionary contains the configurations of the grid connection with the local energy system.
'''
battery_config = {
    'constrained_grid': True,           #
    'grid_capacity': 41.0               # kW        Provide one decimal.
    'fixed_price': False,               #
    'grid_price': 0.20                  # EUR/kWh   Provide one decimal.
}