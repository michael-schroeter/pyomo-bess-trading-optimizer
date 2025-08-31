import pyomo.environ as pyo

from cost_calculator import calculate_capex, calculate_opex, calculate_depreciation_amount

def define_additional_sums_expr(model):
    def net_cashflow(m):        
        revenue = m.e_TOTAL_REVENUE_SUM
        taxes = m.e_TAX
        opex = m.p_OPEX
        return (revenue - taxes - opex)
    model.e_NET_CASHFLOW = pyo.Expression(rule=net_cashflow)



def define_additional_timeseries_expr(model):
    # calculate battery cycles
    def net_cashflow(m, t):
        opex = calculate_opex()
        
        pass