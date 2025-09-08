import pyomo.environ as pyo


def define_aging_cost_expr(model):
    def aging_cost_rule(model, t):
        specific_aging_cost = model.p_SPECIFIC_AGING_COST
        return specific_aging_cost * model.v_CYCLES_EQ[t]

    model.e_AGING_COST     = pyo.Expression(model.T, rule=aging_cost_rule)
    model.e_AGING_COST_SUM = pyo.Expression(expr=sum(model.e_AGING_COST[t] for t in model.T))
