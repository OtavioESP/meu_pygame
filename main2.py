from enum import Enum
from utils.enums import Card
# Load all cards into the `teste` list
teste = [(card.card_name, card.card_value) for card in Card]

# Optional: print to verify
for name, value in teste:
    print(f"Card: {name}, Value: {value}")
