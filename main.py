import pygame
import sys
import time

from random import choice

from utils.enums import Card
from utils.consts import *

CLICK_COOLDOWN = 1.0
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Game")

# Game state
last_click_times = {
    "more_card": 0,
    "enough": 0
}
available_cards = [(card.card_name, card.card_value) for card in Card]
player_cards = []
current_bet = 10
score = 0
cards_sum = 0

more_card_btn = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
enough_btn = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, 370, BUTTON_WIDTH, BUTTON_HEIGHT)

font = pygame.font.SysFont('Arial', 24)

def draw_card(x, y, card, face_up=True):
    """Draw a card at position (x,y)"""
    if face_up:
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 100, 150))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 150), 2)
        text = font.render(f"{card[0]}", True, (0, 0, 0))
        value_text = font.render(f"Value: {card[1]}", True, (0, 0, 0))
        screen.blit(text, (x + 10, y + 10))
        screen.blit(value_text, (x + 10, y + 40))
    else:
        pygame.draw.rect(screen, (200, 0, 0), (x, y, 100, 150))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 150), 2)

def draw_ui():
    """Draw the game interface"""
    # Score and bet info
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    bet_text = font.render(f"Bet: ${current_bet}", True, (255, 255, 0))
    cards_sum_text = font.render(f"Score: {cards_sum}", True, (255, 255, 0))
    screen.blit(score_text, (20, 20))
    screen.blit(bet_text, (20, 50))
    screen.blit(cards_sum_text, (20, 80))

    # Draw player cards
    for i, card in enumerate(player_cards):
        draw_card(150 + i * 30, 300 + (i * 10), card)

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()

    def draw_button(rect, text):
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text_surf = font.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    draw_button(more_card_btn, "More 1 card")
    draw_button(enough_btn, "Enough")


def deal_card():
    """Deal a random card to player"""
    if available_cards:
        card = choice(available_cards)
        player_cards.append(card)
        available_cards.remove(card)
        cards_sum += card[1]
        return card
    return None

def reset_game():
    """Reset game state"""
    global available_cards, player_cards, score
    available_cards = [(card.card_name, card.card_value) for card in Card]
    player_cards = []
    score = 0
    # Deal initial cards
    deal_card()
    deal_card()

def main():
    global current_bet, score
    
    reset_game()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    deal_card()
                elif event.key == pygame.K_r:
                    reset_game()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            current_time = time.time()

            if more_card_btn.collidepoint(event.pos):
                if current_time - last_click_times["more_card"] >= CLICK_COOLDOWN:
                    deal_card()
                    # if check_sum():
                    if cards_sum > 21:
                        # game_over = True
                        reset_game()
                    last_click_times["more_card"] = current_time

            elif enough_btn.collidepoint(event.pos):
                if current_time - last_click_times["enough"] >= CLICK_COOLDOWN:
                    print("Player chose to stop.")
                    last_click_times["enough"] = current_time  # You can replace this with logic later

        # Draw everything
        screen.fill((0, 100, 0))  # Green table
        draw_ui()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()