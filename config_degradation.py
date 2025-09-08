import math
import numpy as np
from params.scenario_config import INITIAL_BATTERY_CAPACITY, EFFICIENCY_BAT, LIFETIME_CYCLES


## Cycle eq ## 
eps = 1e-6
soc_bin_bounds = {
    0: (0.00, 0.25 - eps),
    1: (0.25, 0.50 - eps),
    2: (0.50, 0.75 - eps),
    3: (0.75, 1.00 + eps),
}

SOC_FACTORS = {0: 1.18991, 1: 1.03264, 2: 1.0, 3: 1.56676}



## Capacity Degradation ##
# cal
BATTERY_DEGRADATION_CAL_VALUE = INITIAL_BATTERY_CAPACITY * 0.0033041117323577 / 100 / 96 # abhängig von zyklen/pro tag bzw märkte

# cycle
def c_rest(cycles_eq_cumsum):
    return (
        (
            4.26384996637378232975 * math.exp(-0.00235433534616526522 * cycles_eq_cumsum)
            + 251.46065636316288305352 * math.exp(-0.00000531056139597996 * cycles_eq_cumsum)
            - 155.72450632953666627145
        ) / 100
    )

cap_deg_c_rate_factors = {
    1.0: 0.0, 
    0.5: 1.1634
}

cycle_breakpoints = np.linspace(0, LIFETIME_CYCLES*2, 11).tolist()




## Efficiency Degradation ##
# cal
EFFICIENCY_DEGRADATION_CAL_VALUE = (2.714 * 10**(-6) / 100) * EFFICIENCY_BAT # pro 15min

# cycle
def calculate_efficiency_bat_rest(cycles_cumsum, factor_crate):
        factor = (1.97192 * 10**(-6))  / 100 * factor_crate # pro Cycle
        n = EFFICIENCY_BAT
        v = -factor*EFFICIENCY_BAT
        return  v*cycles_cumsum + n - EFFICIENCY_DEGRADATION_CAL_VALUE


eff_deg_c_rate_factors = {
    1.0: 0.0,
    1/2: 2.9853,
    1/3: 3.6226,
}
