import pygame
import sys
from game.game_engine import GameEngine

# Initialize pygame / Start application
pygame.init()
pygame.mixer.init()  # initialize mixer for sound (safe even if no sounds present)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Create engine (GameEngine will use fonts and sounds; pygame.init() already called)
engine = GameEngine(WIDTH, HEIGHT, target_score=5)

def draw_center_text(surface, text, font, color, y):
    """Helper to draw centered text along x axis at y."""
    rendered = font.render(text, True, color)
    surface.blit(rendered, ((surface.get_width() - rendered.get_width()) // 2, y))

def show_game_over_screen(screen, engine):
    """Show winner and replay options; return chosen target_score or None for quit."""
    overlay = pygame.Surface((engine.width, engine.height))
    overlay.set_alpha(230)
    overlay.fill((10, 10, 10))
    screen.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("Arial", 48)
    small_font = pygame.font.SysFont("Arial", 28)
    winner = engine.check_winner()
    if winner is None:
        title = "Game Over"
    else:
        title = f"{winner} Wins!"

    draw_center_text(screen, title, title_font, WHITE, engine.height // 2 - 80)

    draw_center_text(screen, "Play again? Choose Best of: 3  5  7", small_font, WHITE, engine.height // 2 - 10)
    draw_center_text(screen, "Press ESC to Quit", small_font, WHITE, engine.height // 2 + 30)
    pygame.display.flip()

    # Wait for user choice
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    return 3
                if event.key == pygame.K_5:
                    return 5
                if event.key == pygame.K_7:
                    return 7
                if event.key == pygame.K_ESCAPE:
                    return None
        clock.tick(30)

def main():
    running = True
    while running:
        # Normal event loop and frame update
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()

        SCREEN.fill(BLACK)
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

        # If game reached end, show game-over screen & replay options
        if engine.is_game_over():
            choice = show_game_over_screen(SCREEN, engine)
            if choice is None:
                running = False
            else:
                # replay with new "best of" => target_score = ceil(choice/2)
                engine.reset_for_replay(best_of=choice)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
