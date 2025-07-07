import pyomo.environ as pyo
from cost_calculator import calculate_specific_aging_cost


def define_aging_cost_expr(model):
    def aging_cost_rule(model, t):
        specific_aging_cost = calculate_specific_aging_cost()
        return specific_aging_cost * (model.e_TOTAL_CHARGE[t] + model.e_TOTAL_DISCHARGE[t]) 

    model.e_AGING_COST     = pyo.Expression(model.T, rule=aging_cost_rule)
    model.e_AGING_COST_SUM = pyo.Expression(expr=sum(model.e_AGING_COST[t] for t in model.T))
