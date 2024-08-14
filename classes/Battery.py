import numpy as np
import pulp

from dictionaries.battery_config import *
from dictionaries.systemwide_config import *


class Battery:

    def __init__(self):
        """
        Set up decision variables for optimisation.
        These are the hourly charge and discharge flows for the optimisation horizon, with their limitations.
        """
        self.time_horizon = systemwide_config["time_horizon"]

        self.charge = pulp.LpVariable.dicts(
            "charging_power",
            ("c_t_" + str(i) for i in range(0, systemwide_config["time_horizon"])),
            lowBound=0,
            upBound=battery_config["charge_rate"],
            cat="Continuous",
        )

        self.discharge = pulp.LpVariable.dicts(
            "discharging_power",
            ("d_t_" + str(i) for i in range(0, systemwide_config["time_horizon"])),
            lowBound=0,
            upBound=battery_config["discharge_rate"],
            cat="Continuous",
        )
