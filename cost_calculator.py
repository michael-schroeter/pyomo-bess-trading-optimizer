from params.scenario_config import (
    LIFETIME_CYCLES,
    BATTERY_INVEST,
    INVERTER_INVEST,
    TRANSFORMER_INVEST,
    CONSTRUCTION_ALLOWANCE_INVEST,
    GRID_CONNECTION_INVEST,
    INSURANCE_EXTENSION,
    DC_REST_INVEST,
    FUNDAMENT_INVEST,

    INSURANCE_RATE,
    OPEX_COST,
    DEPRECIATION_YEARS,
)



def calculate_capex():
    battery_cost = BATTERY_INVEST  
    inverter_cost = INVERTER_INVEST   
    dc_rest = DC_REST_INVEST

    fundament_cost = FUNDAMENT_INVEST
    transformer_cost = TRANSFORMER_INVEST  
    construction_allowance = CONSTRUCTION_ALLOWANCE_INVEST  
    grid_connection_cost = GRID_CONNECTION_INVEST 
    insurance_extension = INSURANCE_EXTENSION  
    capex = (
        battery_cost + inverter_cost + dc_rest + fundament_cost +
        transformer_cost + construction_allowance + grid_connection_cost + 
        insurance_extension
    )
    
    return capex


def calculate_opex_per_month():
    capex = calculate_capex()
    insurance_cost = INSURANCE_RATE * (capex - CONSTRUCTION_ALLOWANCE_INVEST - GRID_CONNECTION_INVEST) # nur Hardware wird versichert
    opex = OPEX_COST  # jährliche Betriebskosten

    total_opex = (
        insurance_cost + opex
    )
    opex_per_month = total_opex / 12  # monatliche OPEX
    return opex_per_month


def calculate_depreciation_amount_per_month():
    capex = calculate_capex()
    depreciation_amount = capex / DEPRECIATION_YEARS
    depreciation_amount_per_month = depreciation_amount / 12 
    return depreciation_amount_per_month


def calculate_specific_aging_cost():
    capex = calculate_capex()
    return capex / LIFETIME_CYCLES   # €/cycle_eq




if __name__ == "__main__":
    print("CAPEX:", calculate_capex())
    print("OPEX:", calculate_opex_per_month())
    print("Depreciation Amount:", calculate_depreciation_amount_per_month())
    print("Specific Aging Cost:", calculate_specific_aging_cost())
