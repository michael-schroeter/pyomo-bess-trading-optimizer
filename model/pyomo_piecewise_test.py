import pyomo.environ as pyo

# Angenommene Datenpunkte für Ihre Funktion z = f(x,y)
# (x, y, z)
points = {
    (0, 0): 0,
    (0, 1): 1,
    (1, 0): 2,
    (1, 1): 1.5,
    # ... weitere Punkte, die das Gitter definieren
}

model = pyo.ConcreteModel()

# Ihre zwei unabhängigen Variablen
model.x = pyo.Var(bounds=(0, 1))
model.y = pyo.Var(bounds=(0, 1))

# Die abhängige Variable
model.z = pyo.Var()

# Extrahieren der x- und y-Koordinaten für die Domänen
x_domain = sorted(list(set(x for x, y in points.keys())))
y_domain = sorted(list(set(y for x, y in points.keys())))

# Die Funktionswerte an den Gitterpunkten
f_values = [[points[x, y] for y in y_domain] for x in x_domain]

# Definition der Piecewise-Nebenbedingung
# 'PW_FUNCTION_TYPE.SOS2' ist hier der Schlüssel
# Das gesamte Tupel (model.z, model.x, model.y) ist das ERSTE Argument.
model.pw_constraint = pyo.Piecewise(
    model.z, model.x, model.y,          # RICHTIG: Das sind DREI separate Argumente
    pw_indices=(x_domain, y_domain),
    pw_repn='sos2',
    f_rule=f_values
)

# Beispiel-Zielfunktion und Solver
model.obj = pyo.Objective(expr=model.z, sense=pyo.maximize)
solver = pyo.SolverFactory('gurobi') # oder ein anderer Solver, der SOS2 unterstützt
solver.solve(model)

print(f"x = {pyo.value(model.x)}")
print(f"y = {pyo.value(model.y)}")
print(f"z = {pyo.value(model.z)}")