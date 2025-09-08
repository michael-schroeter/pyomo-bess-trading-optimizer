import pyomo.environ as pyo
from cost_calculator import calculate_depreciation_amount_per_month, calculate_opex_per_month

def add_tax_constraints(model):
    """ tax_base = max(0, profit - s) """
    depreciation = model.p_DEPRECIATION_AMOUNT
    opex = model.p_OPEX
    revenue = model.e_TOTAL_REVENUE_SUM
    model.c_TAX1 = pyo.Constraint(expr = model.v_TAX_BASE >= revenue - depreciation - opex) # monthly values
    model.c_TAX2 = pyo.Constraint(expr = model.v_TAX_BASE >= 0)