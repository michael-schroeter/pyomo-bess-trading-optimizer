from .marketchoice import add_market_choice_constraint
from .prl import add_prl_energy_constraints
from .srl import add_srl_energy_constraints
from .cumulative_energy import add_cumulative_stored_energy_constraints
from .tax import add_tax_constraints
from .battery_degradation import add_battery_degradation_constraints
from .cycles import add_cycles_real_constraints, add_cycles_eq_piecewise_constraints
from .stress import add_stress_constraint, add_soc_stress_factor_constraint, add_power_stress_factor_constraint


def add_all_constraints(model, time_points):
    add_market_choice_constraint(model, time_points) # hier steckt market, prl_mode und srl_mode constraint drin
    add_prl_energy_constraints(model)
    add_srl_energy_constraints(model)
    add_tax_constraints(model)
    add_cumulative_stored_energy_constraints(model)
    add_cycles_real_constraints(model)
    add_cycles_eq_piecewise_constraints(model)
    add_soc_stress_factor_constraint(model)
    add_power_stress_factor_constraint(model)
    add_stress_constraint(model)
    add_battery_degradation_constraints(model)
    return model


