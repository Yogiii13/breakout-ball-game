import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#define game variables
cols = 8
rows = 6

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Paddle class
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 30
        self.speed = 7

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, [self.x, self.y, self.width, self.height])

# Ball class
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed_x = 4 * random.choice((1, -1))
        self.speed_y = -4

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Wall collision
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.y < 0:
            self.speed_y *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

# Brick class
class Brick:
    def __init__(self, x, y):
        self.width = SCREEN_WIDTH // cols
        self.height = 25
        self.x = x
        self.y = y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.destroyed = False

    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])

# Collision detection
def check_collision(ball, paddle, bricks):
    # Ball and paddle collision
    if paddle.y < ball.y + ball.radius < paddle.y + paddle.height:
        if paddle.x < ball.x < paddle.x + paddle.width:
            ball.speed_y *= -1

    # Ball and bricks collision
    for brick in bricks:
        if not brick.destroyed:
            if brick.y < ball.y < brick.y + brick.height:
                if brick.x < ball.x < brick.x + brick.width:
                    ball.speed_y *= -1
                    brick.destroyed = True
                    return 1
    return 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout Ball")
        self.clock = pygame.time.Clock()
        self.state = "main_menu"
        self.high_score = 0
        self.reset_game()

        # Load and scale the background image
        self.background_image = pygame.image.load('background.png')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = [Brick(i * 100 + 10, j * 30 + 50) for i in range(8) for j in range(6)]
        self.score = 0
        self.lives = 3
        self.game_over = False

    def main_menu(self):
        font = pygame.font.Font(None, 74)
        title_text = font.render("Breakout Ball Game", True, WHITE)
        start_text = font.render("Start Game", True, YELLOW)
        high_score_text = font.render("High Score", True, YELLOW)
        exit_text = font.render("Exit", True, YELLOW)

        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, 500))

        while self.state == "main_menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "exit"
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        self.reset_game()
                        self.state = "game"
                    elif high_score_rect.collidepoint(event.pos):
                        self.state = "high_score"
                    elif exit_rect.collidepoint(event.pos):
                        self.state = "exit"
                        return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.reset_game()
                        self.state = "game"
                    elif event.key == pygame.K_2:
                        self.state = "high_score"
                    elif event.key == pygame.K_3:
                        self.state = "exit"
                        return

            self.screen.blit(self.background_image, [0, 0])
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
            self.screen.blit(start_text, start_rect.topleft)
            self.screen.blit(high_score_text, high_score_rect.topleft)
            self.screen.blit(exit_text, exit_rect.topleft)

            pygame.display.flip()
            self.clock.tick(60)

    def display_high_score(self):
        font = pygame.font.Font(None, 74)
        high_score_text = font.render(f"High Score: {self.high_score}", True, WHITE)
        back_text = font.render("Press B to go back", True, YELLOW)

        while self.state == "high_score":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "exit"
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.state = "main_menu"

            self.screen.blit(self.background_image, [0, 0])
            self.screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 200))
            self.screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 400))

            pygame.display.flip()
            self.clock.tick(60)

    def game_loop(self):
        font = pygame.font.Font(None, 36)
        back_text = font.render("Back", True, WHITE)
        back_rect = back_text.get_rect(topleft=(20, 0))

        while self.state == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = "exit"
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        self.state = "main_menu"

            keys = pygame.key.get_pressed()
            if self.game_over:
                if keys[pygame.K_SPACE]:
                    self.reset_game()
            else:
                if keys[pygame.K_LEFT]:
                    self.paddle.move_left()
                if keys[pygame.K_RIGHT]:
                    self.paddle.move_right()

                self.ball.move()
                self.score += check_collision(self.ball, self.paddle, self.bricks)

                # Ball and bottom collision
                if self.ball.y > SCREEN_HEIGHT:
                    self.lives -= 1
                    self.ball = Ball()
                    if self.lives == 0:
                        self.game_over = True
                        if self.score > self.high_score:
                            self.high_score = self.score

            self.screen.blit(self.background_image, [0, 0])

            # Draw objects
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)

            # Display score, lives, and back to home button
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            lives_text = font.render(f"Lives: {self.lives}", True, WHITE)
            self.screen.blit(score_text, (20, 20))
            self.screen.blit(lives_text, (700, 20))
            self.screen.blit(back_text, back_rect.topleft)

            if self.game_over:
                game_over_text = font.render("Game Over! Press Space to Restart", True, WHITE)
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

            # Update screen
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        while self.state != "exit":
            if self.state == "main_menu":
                self.main_menu()
            elif self.state == "high_score":
                self.display_high_score()
            elif self.state == "game":
                self.game_loop()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
