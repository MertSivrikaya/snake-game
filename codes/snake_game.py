import pygame
from pygame.sprite import AbstractGroup
from settings import *
from snake import *

class SnakeGame:
    def __init__(self, display_screen):
        # Creating the snake
        self.snake = Snake()

        # Creating a sprite group for the apple
        self.apple_on_screen = pygame.sprite.GroupSingle(Apple(pygame.Vector2(15,10)))

        # Variable to determine whether the game is running or not
        self.game_active = True

        # Display screen
        self.display_screen = display_screen

        # Variable to keep track of the player score. It will increase every time a new Apple object is created; that is, when the snake collides with an apple.
        self.player_score = 0

    def run(self):
        if self.snake.is_colliding_with_the_screen_borders() or self.snake.is_colliding_with_itself():
            self.game_active = False

        # Seting up the display surface
        self.display_screen.fill("Black")

        # Setting up the sprites on the display screen
        self.snake.body_parts.draw(self.display_screen)
        self.apple_on_screen.draw(self.display_screen)

        # Getting user input to control the snake
        self.snake.get_input()

    def display_end_game_screen(self):
        self.display_screen.fill("Black")

        font = pygame.font.Font("./fonts/Pixeltype.ttf", 40)
        game_over_text = font.render("Game Over!", False, "White")
        game_over_text_rect = game_over_text.get_rect(midtop = (SCREEN_WIDTH / 2, 50))

        score_text = font.render(f"Score: {self.player_score}", False, "White")
        score_text_rect = score_text.get_rect(midtop = (SCREEN_WIDTH / 2, 150))

        info_text = font.render("Press 'Space' to Play Again", False, "White")
        info_text_rect = info_text.get_rect(midtop = (SCREEN_WIDTH / 2, 300))

        self.display_screen.blit(game_over_text, game_over_text_rect)
        self.display_screen.blit(score_text, score_text_rect)
        self.display_screen.blit(info_text, info_text_rect)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.restart_game()

    def restart_game(self):
        # Replace the sprites on the display screen
        self.snake = Snake()
        self.apple_on_screen = pygame.sprite.GroupSingle(Apple(pygame.Vector2(15,10)))

        self.game_active = True
        self.player_score = 0
        
    def create_new_apple(self):
        new_pos_on_grid_x = randint(0, TOTAL_TILES_IN_A_ROW - 1) 
        new_pos_on_grid_y = randint(0, TOTAL_TILES_IN_A_ROW - 1) 

        while (new_pos_on_grid_x, new_pos_on_grid_y) in self.snake.get_body_parts_positions(): # don't place the apple on the snake's body parts
            new_pos_on_grid_x = randint(0, TOTAL_TILES_IN_A_ROW - 1) 
            new_pos_on_grid_y = randint(0, TOTAL_TILES_IN_A_ROW - 1)

        self.apple_on_screen.add(Apple(pygame.Vector2(new_pos_on_grid_x, new_pos_on_grid_y))) # replace the sprite in GroupSingle
        self.player_score += 1