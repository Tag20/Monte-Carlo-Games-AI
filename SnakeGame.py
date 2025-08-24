import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Snake Class
class Snake:
    def __init__(self):
        self.body = [(5, 5)]
        self.direction = RIGHT
        self.food_eaten = 0

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if new_head in self.body or not (0 <= new_head[0] < WIDTH // GRID_SIZE and 0 <= new_head[1] < HEIGHT // GRID_SIZE):
            return False  # Game Over
        self.body.insert(0, new_head)
        return True

    def grow(self):
        self.food_eaten += 1  # Track food eaten

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:  # Prevent reversing
            self.direction = direction

# Food Class
class Food:
    def __init__(self):
        self.position = (random.randint(0, WIDTH // GRID_SIZE - 1), random.randint(0, HEIGHT // GRID_SIZE - 1))

    def respawn(self):
        self.position = (random.randint(0, WIDTH // GRID_SIZE - 1), random.randint(0, HEIGHT // GRID_SIZE - 1))

# Monte Carlo Tree Search (MCTS) for Snake Movement
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def best_child(self):
        if self.children:
            return max(self.children, key=lambda child: child.value / (child.visits + 1e-6))
        return None

    def expand(self, snake_body, food_position):
        for direction in DIRECTIONS:
            new_state = (self.state[0] + direction[0], self.state[1] + direction[1])
            if 0 <= new_state[0] < WIDTH // GRID_SIZE and 0 <= new_state[1] < HEIGHT // GRID_SIZE:
                self.children.append(MCTSNode(new_state, parent=self))

    def simulate(self, food_position, snake_body):
        simulated_state = self.state
        steps = 0
        reward = 0
        while steps < 10:
            if simulated_state == food_position:
                return 10  # Positive reward for eating food
            if simulated_state in snake_body:
                return -10  # Negative reward for hitting itself
            if not (0 <= simulated_state[0] < WIDTH // GRID_SIZE and 0 <= simulated_state[1] < HEIGHT // GRID_SIZE):
                return -10  # Negative reward for hitting the wall
            simulated_state = (simulated_state[0] + random.choice(DIRECTIONS)[0], simulated_state[1] + random.choice(DIRECTIONS)[1])
            steps += 1
            reward -= 1  # Small penalty for longer paths
        return reward

    def backpropagate(self, reward):
        self.visits += 1
        self.value += reward
        if self.parent:
            self.parent.backpropagate(reward)

# Get Best Move using MCTS
def get_best_move(snake, food):
    root = MCTSNode(snake.body[0])
    for _ in range(100):  # Iterations for better decision-making
        node = root
        while node.children:
            node = node.best_child()
        node.expand(snake.body, food.position)
        for child in node.children:
            reward = child.simulate(food.position, snake.body)
            child.backpropagate(reward)
    best_child = root.best_child()
    if best_child:
        best_move = (best_child.state[0] - root.state[0], best_child.state[1] - root.state[1])
        return best_move
    return snake.direction

# Main Game Function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    running = True
    
    while running:
        screen.fill(BLACK)
        pygame.event.pump()
        
        # Handle user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get best move using MCTS
        best_move = get_best_move(snake, food)
        snake.change_direction(best_move)
        
        # Move Snake
        if not snake.move():
            running = False  # Game Over
        
        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()
        else:
            snake.body.pop()
        
        # Draw Snake
        for segment in snake.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        # Draw Food
        pygame.draw.rect(screen, RED, (food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        pygame.display.flip()
        clock.tick(5)  # Adjust speed for better visualization
        
        # Exit when the snake eats 20 food items
        if snake.food_eaten >= 20:
            running = False
    
    time.sleep(2)  # Pause before exiting
    pygame.quit()

if __name__ == "__main__":
    main()