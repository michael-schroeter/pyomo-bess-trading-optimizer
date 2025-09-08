import pyomo.environ as pyo

# ---- Helper: globale Bounds aus indizierter Var ableiten ----
def get_global_bounds(var, index_set):
    """Ermittelt (lb, ub) aus var[t].lb/ub.
       Nimmt konstante Bounds an; sonst werden min/max über T verwendet."""
    lbs, ubs = [], []
    for t in index_set:
        lb = var[t].lb
        ub = var[t].ub
        if lb is None or ub is None:
            raise ValueError(f"Fehlende Bounds bei {var.name}[{t}]")
        lbs.append(lb); ubs.append(ub)
    # Falls überall gleich: nimm den Wert, sonst min/max
    lb_unique = lbs[0] if all(lb == lbs[0] for lb in lbs) else min(lbs)
    ub_unique = ubs[0] if all(ub == ubs[0] for ub in ubs) else max(ubs)
    return float(lb_unique), float(ub_unique)



def get_bat_deg_factor(c_rate: float, factors) -> float:
    if 0.9 <= c_rate <= 1.1:
        return factors[1.0]
    # sonst -> Faktor für 0.5
    return factors[0.5]

def get_eff_deg_factor(c_rate: float, factors) -> float:
    closest_key = min(factors.keys(), key=lambda k: abs(k - c_rate))
    return factors[closest_key]


if __name__ == "__main__":
    c_rate = 0.9
    bat = get_bat_deg_factor(c_rate)
    eff = get_eff_deg_factor(c_rate)
    print(f"bat: {bat}, eff: {eff}")

