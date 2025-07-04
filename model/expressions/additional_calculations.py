import pyomo.environ as pyo

from params import BAT_CAPACITY
from cost_calculator import calculate_capex, calculate_opex, calculate_depreciation_amount

def define_additional_sums_expr(model):
    # calculate battery cycles
    def calc_battery_cycles(m):
        return (m.e_TOTAL_CHARGE_SUM + m.e_TOTAL_DISCHARGE_SUM) / (2 * BAT_CAPACITY)
    model.e_BATTERY_CYCLES = pyo.Expression(rule=calc_battery_cycles)



def define_additional_timeseries_expr(model):
    # calculate battery cycles
    def net_cashflow(m, t):
        opex = calculate_opex()
        
        pass