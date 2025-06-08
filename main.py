import pygame
import sys
import time
import os

from random import choice

from utils.enums import Card
from utils.consts import *

CLICK_COOLDOWN = 1.0
# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Game")

# Load background
background = pygame.image.load(os.path.join('assets', 'BACKGROUND_LARGER.png'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load card sprites
card_sprites = {}
card_back = pygame.image.load(os.path.join('assets', 'PRETO_VERSO.png'))
card_back = pygame.transform.scale(card_back, (100, 150))

# Load all card sprites
for card in Card:
    sprite_path = os.path.join('assets', f"{card.card_name}.png")
    if os.path.exists(sprite_path):
        sprite = pygame.image.load(sprite_path)
        sprite = pygame.transform.scale(sprite, (100, 150))
        card_sprites[card.card_name] = sprite

# Game state
last_click_times = {
    "more_card": 0,
    "enough": 0,
    "new_game": 0
}
available_cards = [(card.card_name, card.card_value) for card in Card]
player_cards = []
table_cards = []
player_sum = 0
table_sum = 0
is_player_turn = True
game_over = False
game_result = None

# Button positions
more_card_btn = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
enough_btn = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, 470, BUTTON_WIDTH, BUTTON_HEIGHT)
new_game_btn = pygame.Rect(WIDTH - BUTTON_WIDTH - BUTTON_PADDING, 540, BUTTON_WIDTH, BUTTON_HEIGHT)

font = pygame.font.SysFont('Arial', 24)
title_font = pygame.font.SysFont('Arial', 36)

def draw_card(x, y, card, face_up=True):
    """Draw a card at position (x,y)"""
    if face_up:
        sprite = card_sprites.get(card[0])
        if sprite:
            screen.blit(sprite, (x, y))
    else:
        screen.blit(card_back, (x, y))

def draw_ui():
    """Draw the game interface"""
    # Game status at the top
    if game_over:
        result_text = title_font.render(game_result, True, (255, 0, 0))  # Red color
        text_rect = result_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))  # Center of screen, moved up
        screen.blit(result_text, text_rect)
    else:
        turn_text = title_font.render(f"Turno: {'Jogador' if is_player_turn else 'Mesa'}", True, (255, 255, 255))
        text_rect = turn_text.get_rect(center=(WIDTH//2, 50))
        screen.blit(turn_text, text_rect)

    # Player and table scores - centered vertically
    player_sum_text = font.render(f"Cartas do Jogador: {player_sum}", True, (255, 255, 0))
    table_sum_text = font.render(f"Cartas da Mesa: {table_sum}", True, (255, 255, 0))
    
    # Position scores vertically centered on the left side
    score_y = HEIGHT // 2 - 50  # Center of screen minus offset
    screen.blit(player_sum_text, (50, score_y))  # Changed from WIDTH - 200 to 50
    screen.blit(table_sum_text, (50, score_y + 30))  # Changed from WIDTH - 200 to 50

    # Calculate starting positions for cards to center them
    card_width = 100
    card_spacing = 120
    total_cards_width = max(len(player_cards), len(table_cards)) * card_spacing
    start_x = (WIDTH - total_cards_width) // 2 + card_width // 2

    # Draw table cards
    for i, card in enumerate(table_cards):
        draw_card(start_x + i * card_spacing, 150, card)

    # Draw player cards
    for i, card in enumerate(player_cards):
        draw_card(start_x + i * card_spacing, 400, card)

    # Draw buttons
    mouse_pos = pygame.mouse.get_pos()

    def draw_button(rect, text):
        color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text_surf = font.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

    if is_player_turn and not game_over:
        draw_button(more_card_btn, "Mais uma carta")
        draw_button(enough_btn, "Parar")
    
    if game_over:
        draw_button(new_game_btn, "Novo Jogo")

def deal_card(is_player=True):
    """Deal a random card to player or table"""
    global player_sum, table_sum
    if available_cards:
        card = choice(available_cards)
        if is_player:
            player_cards.append(card)
            player_sum += card[1]
        else:
            table_cards.append(card)
            table_sum += card[1]
        available_cards.remove(card)
        return card
    return None

def check_winner():
    """Check who won the game"""
    global game_result
    
    if player_sum > 21:
        game_result = "A mesa ganhou! Você perdeu estourou!"
    elif table_sum > 21:
        game_result = "Você ganhou, a mesa estourou! Parabéns!"
    elif player_sum > table_sum:
        game_result = "Voce Ganhou!"
    elif table_sum > player_sum:
        game_result = "A mesa ganhou!"
    else:
        game_result = "Empate!"
    
    return game_result

def table_turn():
    """Handle table's turn"""
    global is_player_turn, game_over
    
    while table_sum < 21:  # Table will keep drawing until it reaches at least 17
        deal_card(is_player=False)
        pygame.time.wait(1000)  # Wait 1 second between draws
        screen.blit(background, (0, 0))  # Draw background instead of filling with green
        draw_ui()
        pygame.display.flip()
    
    game_over = True
    check_winner()

def reset_game():
    """Reset game state"""
    global available_cards, player_cards, table_cards, player_sum, table_sum
    global is_player_turn, game_over, game_result
    
    # Clear the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    available_cards = [(card.card_name, card.card_value) for card in Card]
    player_cards = []
    table_cards = []
    player_sum = 0
    table_sum = 0
    is_player_turn = True
    game_over = False
    game_result = None
    
    # Deal initial cards
    deal_card(is_player=True)
    deal_card(is_player=True)
    deal_card(is_player=False)  # Deal one card to table

def main():
    global is_player_turn, game_over
    
    reset_game()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                current_time = time.time()

                if game_over and new_game_btn.collidepoint(event.pos):
                    if current_time - last_click_times["new_game"] >= CLICK_COOLDOWN:
                        reset_game()
                        last_click_times["new_game"] = current_time
                
                elif is_player_turn and not game_over:
                    if more_card_btn.collidepoint(event.pos):
                        if current_time - last_click_times["more_card"] >= CLICK_COOLDOWN:
                            deal_card(is_player=True)
                            if player_sum >= 21:
                                is_player_turn = False
                                table_turn()
                            last_click_times["more_card"] = current_time

                    elif enough_btn.collidepoint(event.pos):
                        if current_time - last_click_times["enough"] >= CLICK_COOLDOWN:
                            is_player_turn = False
                            table_turn()
                            last_click_times["enough"] = current_time

        # Draw everything
        screen.blit(background, (0, 0))  # Draw background first
        draw_ui()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()