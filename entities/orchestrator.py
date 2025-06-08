from utils.enums import Card

class Orchestrator:
    
    def __init__(self):
        self.AVAILABLE_CARDS = [(card.card_name, card.card_value) for card in Card]
        self.SCORE = 0
        self.CARDS_SUM = 0
        self.TURN = 0
