from .marketchoice import add_market_choice_constraint
from .prl import add_prl_energy_constraints
from .srl import add_srl_energy_constraints
from .cumulative_energy import add_cumulative_stored_energy_constraints
from .tax import add_tax_constraints
from .battery_degradation import add_battery_degradation_constraints
from .cycles import add_cycles_real_constraints
from .cycles_eq import add_cycles_eq_constraints
from .efficiency_degradation import add_efficiency_degradation_constraints
from .cycle_limits import add_cycle_limit_constraints


def add_all_constraints(model, time_points):
    add_market_choice_constraint(model, time_points) # hier steckt market, prl_mode und srl_mode constraint drin
    add_prl_energy_constraints(model)
    add_srl_energy_constraints(model)
    add_tax_constraints(model)
    add_cumulative_stored_energy_constraints(model)
    add_cycles_real_constraints(model)
    add_cycles_eq_constraints(model)
    add_battery_degradation_constraints(model)
    add_efficiency_degradation_constraints(model)
    add_cycle_limit_constraints(model)
    return model


