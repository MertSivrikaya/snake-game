import pygame, sys
from settings import *
from snake_game import SnakeGame

class Game:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        self.clock = pygame.time.Clock()

        self.snake_game = SnakeGame(self.screen)

        self.snake_move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.snake_move_event, self.snake_game.snake.time_between_moves)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.snake_move_event and self.snake_game.game_active: # snake will move every given milliseconds
                    self.snake_game.snake.move(self.snake_game.apple_on_screen.sprite, self.snake_game.create_new_apple)
           
            if self.snake_game.game_active:
                self.snake_game.run()

            else:
                self.snake_game.display_end_game_screen()

            self.clock.tick()
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
