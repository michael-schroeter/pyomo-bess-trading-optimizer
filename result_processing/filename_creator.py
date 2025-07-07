import uuid
import os

from params.params import (
    MARKET_SWITCH,
    PRL_SWITCH,
    SRL_SWITCH,
    BAT_CAPACITY,
    SYSTEM_POWER,
    BAT_PRICE,
    LIFETIME_CYCLES,
    EFFICIENCY,
    START_DATE,
    END_DATE
)


import uuid
# ... deine anderen Imports

def create_filename():
    # ... (deine Funktion bleibt unverändert)
    return f"results_market-{MARKET_SWITCH}_prl-{PRL_SWITCH}_srl-{SRL_SWITCH}_{BAT_CAPACITY}-MWH_{SYSTEM_POWER}MW_{BAT_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}"


def create_unique_filename() -> str:
    """Erzeugt den Basis-Dateinamen und fügt eine ID und eine Endung hinzu."""
    
    basename = create_filename() 
    random_id = str(uuid.uuid4())[:8]
    unique_filename = f"{basename}_{random_id}"
    
    return unique_filename


if __name__ == "__main__":
    final_filename = create_unique_filename()
    print(final_filename)

