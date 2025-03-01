import pygame
from pygame.sprite import AbstractGroup
from settings import *
from random import randint

BODY_PART_COLOR = "#228b22"
HEAD_COLOR = "#00ff00"

class Apple(pygame.sprite.Sprite):
    def __init__(self, pos_on_grid : pygame.Vector2) -> None:
        super().__init__()
        self.pos_on_grid = pos_on_grid

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("Red")

        self.rect = self.image.get_rect(topleft = (self.pos_on_grid.x * TILE_SIZE, self.pos_on_grid.y * TILE_SIZE))
        
class BodyPart(pygame.sprite.Sprite):
    def __init__(self, pos_on_grid : pygame.Vector2, is_head = False):
        super().__init__()
        self.pos_on_grid = pos_on_grid
        
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if not is_head:
            self.image.fill(BODY_PART_COLOR)
        else:
            self.image.fill(HEAD_COLOR)

        self.rect = self.image.get_rect(topleft = (self.pos_on_grid.x * TILE_SIZE, self.pos_on_grid.y * TILE_SIZE))
        
    def move(self, new_pos_on_grid : pygame.Vector2):
        self.pos_on_grid = new_pos_on_grid.copy() # if we didn't use the method 'copy()' then pos_on_grid would point the same memory adress with the next body part so changing one's position would change the other's position.
        #self.pos_on_grid = pygame.math.Vector2.move_towards()
        self.rect.topleft = (self.pos_on_grid.x * TILE_SIZE, self.pos_on_grid.y * TILE_SIZE)

    def change_to_body(self):
        self.image.fill(BODY_PART_COLOR)

class Snake:
    def __init__(self):
        # Creating a sprite group containing body parts of the snake
        self.body_parts = pygame.sprite.Group()

        # Creating the inital snake
        self.head_position = pygame.Vector2(5,10)
        body_part_before_head = pygame.Vector2(4,10)
        
        self.body_parts.add(BodyPart(body_part_before_head, False))
        self.body_parts.add(BodyPart(self.head_position, True)) # we will add the new snake heads at the end of the list/group

        # The snake will move every given milliseconds
        self.time_between_moves = 125 # milliseconds
       
        # The number of squares the snake will move in each direction in each move
        self.direction_vector = pygame.Vector2(1, 0)

        # This bool will prevent player from changing input multiple times between two moves. Othetwise, the snake could move to directions normally it shouldn't be able to.
        self.can_get_input_until_new_move = True

    def get_input(self):
        keys = pygame.key.get_pressed()

        if self.can_get_input_until_new_move:
            
            if self.direction_vector.y == 0:
                if keys[pygame.K_w]:
                    self.direction_vector = pygame.Vector2((0,-1))
                    self.can_get_input_until_new_move = False
                
                elif keys[pygame.K_s]:
                    self.direction_vector = pygame.Vector2((0,1))
                    self.can_get_input_until_new_move = False

            else:
                if keys[pygame.K_d]:
                    self.direction_vector = pygame.Vector2((1,0))
                    self.can_get_input_until_new_move = False

                elif keys[pygame.K_a]:
                    self.direction_vector = pygame.Vector2((-1,0))
                    self.can_get_input_until_new_move = False
        
    def move(self, apple_on_screen : Apple, create_new_apple):
        # If the snake collides with an apple, don't move the body parts, instead, only add a new head on the position of the apple used have.
        if self.head_position + self.direction_vector == apple_on_screen.pos_on_grid: # if the snakes collides with the apple
            self.add_head(apple_on_screen.pos_on_grid)
            create_new_apple()

        else:
            # Move all body_parts except the head to the latest keyboard input 
            for index, body_part in enumerate(self.body_parts.sprites()):
                if not index == len(self.body_parts.sprites()) - 1:
                    body_part.move(self.body_parts.sprites()[index + 1].pos_on_grid) # Move the body part to the position of next body part's position

            # Move the head
            self.head_position += self.direction_vector
            self.body_parts.sprites()[-1].move(self.head_position) 

        self.can_get_input_until_new_move = True

    def add_head(self, pos : pygame.Vector2):
        self.head_position = pos
        self.body_parts.sprites()[-1].change_to_body() # make the former head's color body color.
        self.body_parts.add(BodyPart(self.head_position, True)) # Add a new head to snake
        
    def get_body_parts_positions(self):
        pos_list = [(sprite.pos_on_grid.x, sprite.pos_on_grid.y) for sprite in self.body_parts.sprites()]
        
        return pos_list

    def is_colliding_with_the_screen_borders(self):
        target_square_pos = self.head_position

        if target_square_pos.x < 0 or target_square_pos.x > TOTAL_TILES_IN_A_ROW - 1:
            return True
        elif target_square_pos.y < 0 or target_square_pos.y > TOTAL_TILES_IN_A_ROW - 1:
            return True
        else:
            return False
        
    def is_colliding_with_itself(self):
        body_part_positions = self.get_body_parts_positions()
        del body_part_positions[-1]

        if (self.head_position.x, self.head_position.y) in body_part_positions:
            return True
        else:
            return False
        


    

