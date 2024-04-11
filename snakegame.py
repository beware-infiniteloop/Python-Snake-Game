import numpy as np
import pygame
import time
import random
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (50, 168, 82)
FONT_COLOR = (255, 255, 255)
speed=0.3

class Apple:
    def __init__(self, surface):
        self.parent_screen = surface
        self.image = pygame.image.load("apple.jpg").convert()
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE
        self.position = np.array([self.x, self.y])
        print(self.position)


class Snake:
    def __init__(self, surface):
        self.parent_screen = surface
        self.block = pygame.image.load("block.jpg").convert()
        self.position = np.array([[40, 40]])
        self.direction = np.array([0, SIZE])
        self.length = 1
        self.apple1 = Apple(surface)
        self.score=0
        self.background_image = pygame.image.load("forest floor.jpg") 
        #sound for eating an apple
        self.eat_sound = pygame.mixer.Sound("eat.mp3")

    def move_left(self):
        if self.direction[0] != SIZE:
            self.direction = np.array([-SIZE, 0])

    def move_right(self):
        if self.direction[0] != -SIZE:
            self.direction = np.array([SIZE, 0])

    def move_up(self):
        if self.direction[1] != SIZE:
            self.direction = np.array([0, -SIZE])

    def move_down(self):
        if self.direction[1] != -SIZE:
            self.direction = np.array([0, SIZE])

    def increase_length(self):
        self.length += 1
        self.position = np.vstack([self.position, [-1, -1]])
        self.score+=10

    def is_collision(self, x1, y1, x2, y2): #only for collision with itself
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def check_collision(self):
        # Check collision with boundaries
        if (self.position[:, 0] < 0).any() or (self.position[:, 0] >= 1000).any() or \
        (self.position[:, 1] < 0).any() or (self.position[:, 1] >= 800).any():
            return True

        # Check collision with itself
        head = self.position[0]
        body = self.position[1:]
        for pos in body:
            if self.is_collision(head[0], head[1], pos[0], pos[1]):
                return True
            
        # Check collision with apple
        if np.all(self.position[0] == self.apple1.position):
            self.increase_length()
            self.apple1.move()
            # Play the eat sound
            pygame.mixer.Sound.play(self.eat_sound)
            return False

        return False

    def walk(self):
        # Move the head of the snake
        self.position = np.vstack([self.position[0] + self.direction, self.position[:-1]])

        # Check for collisions
        if self.check_collision():
            raise Exception("Game over: Snake collided with boundary or itself")

        # Redraw the snake
        self.draw()

    def draw(self):
        self.parent_screen.blit(self.background_image, (0, 0)) 
        for pos in self.position:
            self.parent_screen.blit(self.block, (pos[0], pos[1]))

        self.apple1.draw()

    def draw_score(self):
        font = pygame.font.Font(None, 45)
        score_text = font.render("Score: " + str(self.score), True, FONT_COLOR)
        self.parent_screen.blit(score_text, (20, 20))
        pygame.display.flip()



class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.play_background_music()

    def show_game_over(self):
        self.play_sound("ding")
        font = pygame.font.Font(None, 60)
        game_over_text = font.render("Game Over!", True, FONT_COLOR)
        continue_text = font.render("Press ESC to quit", True, FONT_COLOR)
        game_over_rect = game_over_text.get_rect(center=(500, 300))
        continue_rect = continue_text.get_rect(center=(500, 400))
        score = font.render(f"Score: {self.snake.length*10-10}",True,(200,200,200))
        self.surface.blit(score,(400,200))

        self.surface.blit(game_over_text, game_over_rect)
        self.surface.blit(continue_text, continue_rect)
        pygame.display.flip()

    def play_background_music(self):
        pygame.mixer.music.load('bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("game over.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("game over.mp3")

        pygame.mixer.Sound.play(sound)

    def run(self):
        running = True
        game_over = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if game_over:
                            running = False
                    elif not game_over:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        elif event.key == K_RIGHT:
                            self.snake.move_right()
                        elif event.key == K_UP:
                            self.snake.move_up()
                        elif event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not game_over:
                    self.snake.walk()
                    self.snake.draw_score()
                    # Adjust speed based on snake's length
                    speed = max(0.05, 0.3 - (self.snake.length - 1) * 0.01)
            except Exception as e:
                self.show_game_over()
                game_over = True
            time.sleep(speed)  # Adjust the time here to control the speed

if __name__ == '__main__':
    game = Game()
    game.run()
