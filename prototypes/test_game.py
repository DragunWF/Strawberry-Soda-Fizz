import pygame
import random
import sys

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Strawberry Soda Fizz - Prototype")
clock = pygame.time.Clock()

# --- Colors ---
BG_COLOR = (255, 182, 193)       # Light Pink (Soda)
PLAYER_COLOR = (220, 20, 60)     # Crimson (Strawberry Chunk)
BUBBLE_COLOR = (255, 255, 255)   # White (Carbonation)
HAZARD_COLOR = (255, 215, 0)     # Yellow (Lemon Seed)
TEXT_COLOR = (50, 0, 0)

# --- Classes ---
class Player:
    def __init__(self):
        self.size = 30
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, self.size, self.size)
        self.vel_y = 0
        self.speed_x = 7
        self.gravity = 0.5
        self.jump_power = -12

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed_x

        # Screen wrap-around (cylindrical glass effect)
        if self.rect.right < 0:
            self.rect.left = WIDTH
        elif self.rect.left > WIDTH:
            self.rect.right = 0

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def bounce(self):
        self.vel_y = self.jump_power

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
        # Draw a little green stem for visual flair
        pygame.draw.rect(surface, (34, 139, 34), (self.rect.x + 10, self.rect.y - 5, 10, 5))

class Bubble:
    def __init__(self, x, y):
        self.radius = random.randint(15, 35)
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)
        self.speed_y = random.uniform(1.0, 3.5)

    def update(self):
        self.rect.y -= self.speed_y

    def draw(self, surface):
        pygame.draw.circle(surface, BUBBLE_COLOR, self.rect.center, self.radius)
        # Inner detail to make it look like a bubble
        pygame.draw.circle(surface, BG_COLOR, (self.rect.centerx - 5, self.rect.centery - 5), self.radius // 3)

class Hazard:
    def __init__(self, x, y):
        self.size = 20
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.speed_y = random.uniform(3.0, 6.0)

    def update(self):
        self.rect.y += self.speed_y

    def draw(self, surface):
        # Draw a diamond shape for the lemon seed
        points = [
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.centery),
            (self.rect.centerx, self.rect.bottom),
            (self.rect.left, self.rect.centery)
        ]
        pygame.draw.polygon(surface, HAZARD_COLOR, points)

# --- Game Loop ---
def main():
    player = Player()
    bubbles = [Bubble(random.randint(0, WIDTH-40), HEIGHT - i*100) for i in range(6)]
    hazards = []
    
    score = 0
    font = pygame.font.SysFont(None, 36)
    game_over = False

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    main() # Restart the game

        keys = pygame.key.get_pressed()

        if not game_over:
            # 2. Update Physics & Logic
            player.move(keys)
            player.apply_gravity()

            # Bubble Logic
            for bubble in bubbles:
                bubble.update()
                # If player is falling and hits the top half of a bubble, bounce!
                if player.vel_y > 0 and player.rect.colliderect(bubble.rect):
                    if player.rect.bottom <= bubble.rect.centery + 15:
                        player.bounce()
                        score += 10
                        # Pop the bubble and spawn a new one at the bottom
                        bubbles.remove(bubble)
                        bubbles.append(Bubble(random.randint(0, WIDTH-40), HEIGHT + random.randint(50, 150)))

            # Recycle bubbles that float off the top
            for bubble in bubbles[:]:
                if bubble.rect.bottom < 0:
                    bubbles.remove(bubble)
                    bubbles.append(Bubble(random.randint(0, WIDTH-40), HEIGHT + random.randint(50, 150)))

            # Hazard Logic (Spawn and Update)
            if random.random() < 0.02: # 2% chance per frame to spawn a lemon seed
                hazards.append(Hazard(random.randint(0, WIDTH-20), -50))

            for hazard in hazards[:]:
                hazard.update()
                if hazard.rect.top > HEIGHT:
                    hazards.remove(hazard)
                # Collision with hazard
                if player.rect.colliderect(hazard.rect):
                    game_over = True

            # Camera / Scrolling logic (Keep player from going too high)
            if player.rect.top < HEIGHT // 3:
                offset = (HEIGHT // 3) - player.rect.top
                player.rect.top = HEIGHT // 3
                for bubble in bubbles:
                    bubble.rect.y += offset
                for hazard in hazards:
                    hazard.rect.y += offset
                score += int(offset // 10) # Points for climbing

            # Death by falling flat
            if player.rect.top > HEIGHT:
                game_over = True

        # 3. Drawing
        screen.fill(BG_COLOR)
        
        for bubble in bubbles:
            bubble.draw(screen)
        for hazard in hazards:
            hazard.draw(screen)
            
        player.draw(screen)

        # UI
        score_text = font.render(f"Fizz Level: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        if game_over:
            go_text = font.render("SODA WENT FLAT! Press SPACE", True, TEXT_COLOR)
            text_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(go_text, text_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()