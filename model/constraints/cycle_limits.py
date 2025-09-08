
import pyomo.environ as pyo
from params.scenario_config import MAX_CYCLES_PER_DAY


def add_cycle_limit_constraints(model):

    def cycles_per_day_rule(m, d):
        return sum(m.v_CYCLES[t] for t in m.T_by_day[d]) <= MAX_CYCLES_PER_DAY

    if MAX_CYCLES_PER_DAY is not None and MAX_CYCLES_PER_DAY > 0:
        model.daily_cycles = pyo.Constraint(model.DAYS, rule=cycles_per_day_rule)
    