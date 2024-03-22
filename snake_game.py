import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def move(self):
        head = self.body[0]
        x, y = self.direction
        new_head = ((head[0] + x * CELL_SIZE) % SCREEN_WIDTH, (head[1] + y * CELL_SIZE) % SCREEN_HEIGHT)
        if new_head in self.body:
            return False  # Game over, snake collided with itself
        self.body.insert(0, new_head)
        self.body.pop()  # Remove the tail
        return True

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, BLUE, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Fruit class
class Fruit:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        return (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    fruit = Fruit()
    score = 0

    font = pygame.font.SysFont(None, 30)

    running = True
    game_over = False
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)

        if not game_over:
            if not snake.move():
                game_over = True

            if snake.body[0] == fruit.position:
                snake.grow()
                fruit.position = fruit.generate_position()
                score += 1

        snake.draw(screen)
        fruit.draw(screen)

        # Display Score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over! Press Q to quit.", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 15))

        pygame.display.flip()
        clock.tick()  # Adjust snake speed here

    pygame.quit()

if __name__ == "__main__":
    main()
