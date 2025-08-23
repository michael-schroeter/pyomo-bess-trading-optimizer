from params.scenario_config1 import (
    INITIAL_BATTERY_CAPACITY, 
    LIFETIME_CYCLES,
    SYSTEM_POWER,
    BATTERY_INVEST,
    INVERTER_INVEST,
    TRANSFORMER_INVEST,
    CONSTRUCTION_ALLOWANCE_INVEST,
    GRID_CONNECTION_INVEST,
    INSURANCE_EXTENSION,

    INSURANCE_RATE,
    TECHNICAL_MANAGEMENT_COST,  
    MAINTENANCE_COST,
    REPAIRS_COST,
    MEASUREMENTS_COST,
    ACCOUNTING_COST,
    DEPRECIATION_YEARS,
)



def calculate_capex():
    battery_cost = BATTERY_INVEST  
    inverter_cost = INVERTER_INVEST   
    transformer_cost = TRANSFORMER_INVEST  
    construction_allowance = CONSTRUCTION_ALLOWANCE_INVEST  
    grid_connection_cost = GRID_CONNECTION_INVEST 
    insurance_extension = INSURANCE_EXTENSION  
    capex = (
        battery_cost + inverter_cost + transformer_cost +
        construction_allowance + grid_connection_cost + 
        insurance_extension
    )
    
    return capex


def calculate_opex():
    capex = calculate_capex()
    insurance_cost = INSURANCE_RATE * (capex - CONSTRUCTION_ALLOWANCE_INVEST - GRID_CONNECTION_INVEST) # nur Hardware wird versichert
    technical_management_cost = TECHNICAL_MANAGEMENT_COST 
    maintenance_cost = MAINTENANCE_COST 
    repairs_cost = REPAIRS_COST 
    measurements_cost = MEASUREMENTS_COST
    accounting_cost = ACCOUNTING_COST

    total_opex = (
        insurance_cost + technical_management_cost + maintenance_cost +
        repairs_cost + measurements_cost + accounting_cost
    )
    
    return total_opex


def calculate_depreciation_amount():
    capex = calculate_capex()
    return (capex / DEPRECIATION_YEARS)


def calculate_specific_aging_cost():
    capex = calculate_capex()
    return capex / (INITIAL_BATTERY_CAPACITY * LIFETIME_CYCLES * 2)  # €/(MWh throughput), both charge and discharge



if __name__ == "__main__":
    print("CAPEX:", calculate_capex())
    print("OPEX:", calculate_opex())
    print("Depreciation Amount:", calculate_depreciation_amount())
    print("Specific Aging Cost:", calculate_specific_aging_cost())
    print("System Power:", SYSTEM_POWER)