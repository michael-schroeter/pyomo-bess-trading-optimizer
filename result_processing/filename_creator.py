import uuid
import os

#def create_filename():
    #return f"results_market-{MARKET_SWITCH}_prl-{PRL_SWITCH}_srl-{SRL_SWITCH}_{BAT_CAPACITY}-MWH_{SYSTEM_POWER}MW_{BAT_PRICE}€_LC-{LIFETIME_CYCLES}n_n-{EFFICIENCY}%_{START_DATE}to{END_DATE}"


def create_random_filename() -> str:    
    return str(uuid.uuid4())[:8]


if __name__ == "__main__":
    filename = create_random_filename()
    print(filename)

