import pyomo.environ as pyo
from cost_calculator import calculate_depreciation_amount, calculate_opex

def add_tax_constraints(model):
    """ tax_base = max(0, profit - s) """
    depreciation = calculate_depreciation_amount()
    opex = calculate_opex()
    revenue = model.e_TOTAL_REVENUE_SUM
    model.c_TAX1 = pyo.Constraint(expr = model.v_TAX_BASE >= revenue - depreciation/12 - opex/12)
    model.c_TAX2 = pyo.Constraint(expr = model.v_TAX_BASE >= 0)