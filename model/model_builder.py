import pyomo.environ as pyo
from model.param import define_params
from model.variables import define_variables
from model.expressions import define_all_expressions
from model.constraints import add_all_constraints
from model.objective import define_objective



def solve_model(model):
    solver = pyo.SolverFactory('gurobi')
    solver.options['Threads'] = 4
    solver.options['MIPGap'] = 0.05  # 5% Optimalitätslücke akzeptieren
    solver.options.update({
        'Heuristics': 0.2,     # mehr Startheuristik
        'MIPFocus': 1,         # schneller Machbarkeit finden (oft hilfreich)
        'Presolve': 2,         # aggressiver Presolve
    })

    #solver.options['TimeLimit'] = 10  # Zeitlimit (Sekunden)
    return solver.solve(model, tee=False)



def setup_model(df_data_period, initial_battery_capacity_for_year, initial_cycles, initial_cycles_eq, initial_efficiency, initial_stored_energy):
    time_points = df_data_period.index.tolist()	
    model = pyo.ConcreteModel()
    
    model.T = pyo.Set(initialize=time_points, ordered=True) # 15-Minuten-Zeitschritte
    model.DAYS = pyo.Set(initialize=sorted({t.date() for t in time_points}), ordered=True)
    def _init_T_by_day(m, d):
        return [t for t in time_points if t.date() == d]
    model.T_by_day = pyo.Set(model.DAYS, initialize=_init_T_by_day, ordered=True)

    unique_intervals = sorted({(t.date(), t.hour // 4) for t in time_points})
    model.D4 = pyo.Set(initialize=unique_intervals, ordered=True)
    model.time_to_interval = {t: (t.date(), t.hour // 4) for t in time_points} # ordnet jeden 15-Minuten-Zeitschritt einem 4-Stunden-Intervall zu
    model.interval_to_start_time = { iv: min(t for t, interval in model.time_to_interval.items() if interval == iv)for iv in model.D4} # speichert für jedes 4-Stunden-Intervall den ersten 15-Minuten-Zeitschritt
    model.K = pyo.Set(initialize=range(4), ordered=True)
    
    define_params(model, df_data_period, initial_battery_capacity_for_year, initial_cycles, initial_cycles_eq, initial_efficiency, initial_stored_energy)
    define_variables(model)
    define_all_expressions(model)
    add_all_constraints(model, time_points)
    define_objective(model)

    return model
