import uuid
import os

#def create_filename():
    #return f"results_market-{MARKET_SWITCH}_prl-{PRL_SWITCH}_srl-{SRL_SWITCH}_{BAT_CAPACITY}-MWH_{SYSTEM_POWER}MW_{BAT_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}"


def create_unique_filename() -> str:
    """Erzeugt den Basis-Dateinamen und fügt eine ID und eine Endung hinzu."""
    
    basename = "" 
    random_id = str(uuid.uuid4())[:8]
    unique_filename = f"{basename}_{random_id}"
    
    return unique_filename


if __name__ == "__main__":
    final_filename = create_unique_filename()
    print(final_filename)

