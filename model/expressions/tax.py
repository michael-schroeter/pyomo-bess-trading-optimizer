import pyomo.environ as pyo
from params.scenario_config1 import (
    TAX_RATE,
)


def define_tax_expr(model):
    model.e_TAX = pyo.Expression(expr = TAX_RATE * model.v_TAX_BASE)