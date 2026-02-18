import pygame
import random
import sys

# Constants
GRID_SIZE = 10  # Changed to 10x10
CELL_SIZE = 50  # Adjusted cell size to fit the screen
WIDTH = HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 4  # Lowered from 5 to 4 for slower movement

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("10x10 Snake Challenge")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.state = "START" # Possible states: START, PLAYING, GAMEOVER, WON
        self.reset_data()

    def reset_data(self):
        # Snake starts with 2 segments
        self.snake = [(5, 5), (5, 6)] 
        self.direction = (0, -1) # Moving Up
        self.fruit = self.spawn_fruit()

    def spawn_fruit(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) 
                       if (r, c) not in self.snake]
        return random.choice(empty_cells) if empty_cells else None

    def update(self):
        if self.state != "PLAYING":
            return

        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Check Wall Collision
        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            self.state = "GAMEOVER"
            return

        # Check Self Collision
        if new_head in self.snake:
            self.state = "GAMEOVER"
            return

        self.snake.insert(0, new_head)

        # Check Fruit Eating
        if new_head == self.fruit:
            if len(self.snake) == GRID_SIZE * GRID_SIZE:
                self.state = "WON"
            else:
                self.fruit = self.spawn_fruit()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw subtle grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

        if self.state == "START":
            self.show_message("SNAKE GAME", "Press SPACE to Start")
        elif self.state == "PLAYING":
            # Draw Snake
            for segment in self.snake:
                rect = pygame.Rect(segment[0]*CELL_SIZE+1, segment[1]*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2)
                pygame.draw.rect(self.screen, GREEN, rect)
            # Draw Fruit
            if self.fruit:
                f_rect = pygame.Rect(self.fruit[0]*CELL_SIZE+1, self.fruit[1]*CELL_SIZE+1, CELL_SIZE-2, CELL_SIZE-2)
                pygame.draw.rect(self.screen, RED, f_rect)
        elif self.state == "GAMEOVER":
            self.show_message("GAME OVER", "Press R to Restart")
        elif self.state == "WON":
            self.show_message("YOU WON!", "Press R to Restart")

        pygame.display.flip()

    def show_message(self, main_text, sub_text):
        main_surf = self.font.render(main_text, True, WHITE)
        sub_surf = pygame.font.SysFont("Arial", 20).render(sub_text, True, GREEN)
        
        self.screen.blit(main_surf, (WIDTH//2 - main_surf.get_width()//2, HEIGHT//2 - 40))
        self.screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, HEIGHT//2 + 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if self.state == "START" and event.key == pygame.K_SPACE:
                        self.state = "PLAYING"
                    elif (self.state == "GAMEOVER" or self.state == "WON") and event.key == pygame.K_r:
                        self.reset_data()
                        self.state = "PLAYING"
                    
                    if self.state == "PLAYING":
                        if event.key == pygame.K_UP and self.direction != (0, 1):
                            self.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.direction = (1, 0)

            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()