import pygame
import os
import math
import random
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

def _load_sound(path):
    """Load a sound if available, otherwise return None."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.6)  # Default volume
        return sound
    except Exception as e:
        print(f"[WARN] Could not load sound {path}: {e}")
        return None


class GameEngine:
    def __init__(self, width, height, target_score=5):
        self.width = int(width)
        self.height = int(height)
        self.paddle_width = 10
        self.paddle_height = 100

        player_x = 10
        player_y = (self.height // 2) - (self.paddle_height // 2)
        ai_x = self.width - self.paddle_width - 10
        ai_y = player_y

        self.player = Paddle(player_x, player_y, self.paddle_width, self.paddle_height)
        self.ai = Paddle(ai_x, ai_y, self.paddle_width, self.paddle_height)

        # Ball starts in the center
        self.ball = Ball(self.width // 2, self.height // 2, 12, 12, self.width, self.height)

        self.player_score = 0
        self.ai_score = 0
        self.target_score = int(target_score)

        # Fonts
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 48)

        # Load sounds
        base = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds")
        self.sound_paddle = _load_sound(os.path.join(base, "paddle_hit.wav"))
        self.sound_wall = _load_sound(os.path.join(base, "wall_bounce.wav"))
        self.sound_score = _load_sound(os.path.join(base, "score.wav"))

        # Reset control
        self.reset_cooldown = 0
        self.reset_cooldown_frames = 10

        # Track time for speed ramp
        self.frame_counter = 0

        # Sound trigger flags
        self.last_wall_hit = False
        self.last_paddle_hit = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.player.speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.player.speed
        if dy != 0:
            self.player.move(dy, self.height)

    def update(self):
        # 🔥 Gradually increase ball speed over time
        self.frame_counter += 1
        if self.frame_counter % 180 == 0:  # every ~3 seconds at 60 FPS
            self.ball.speed *= 1.05
        

        # ---- Move the ball and handle wall bounce ----
        wall_event = self.ball.move()
        if wall_event == "wall":
            if not self.last_wall_hit:  # only trigger once per bounce
                if self.sound_wall:
                    self.sound_wall.play()
                self.last_wall_hit = True
        else:
            self.last_wall_hit = False

        # ---- Paddle Collision ----
        if self.reset_cooldown > 0:
            self.reset_cooldown -= 1
        else:
            coll = self.ball.check_collision(self.player, self.ai)
            if coll and not self.last_paddle_hit:
                if self.sound_paddle:
                    self.sound_paddle.play()
                self.last_paddle_hit = True
            elif coll is None:
                self.last_paddle_hit = False

        # ---- Scoring ----
        if self.ball.left() <= 0:
            self.ai_score += 1
            self._play_score_sound()
            self._score_reset(direction=1)
        elif self.ball.right() >= self.width:
            self.player_score += 1
            self._play_score_sound()
            self._score_reset(direction=-1)

        # ---- AI Movement ----
        self.ai.auto_track(self.ball, self.height)

    def _play_score_sound(self):
        """Play scoring sound safely without overlap."""
        if self.sound_score:
            self.sound_score.stop()  # ensure not overlapping
            self.sound_score.play()

    def _score_reset(self, direction=1):
        """Reset ball to center and send toward given direction."""
        self.ball.reset(self.width // 2, self.height // 2)
        self.reset_cooldown = self.reset_cooldown_frames
        angle = random.uniform(-0.3, 0.3)
        self.ball.velocity_x = direction * self.ball.speed * math.cos(angle)
        self.ball.velocity_y = self.ball.speed * math.sin(angle)
        # Reset sound flags so new events work normally
        self.last_wall_hit = False
        self.last_paddle_hit = False

    def render(self, screen):
        # Draw objects
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())

        # Center line
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4 - player_text.get_width() // 2, 20))
        screen.blit(ai_text, (self.width * 3 // 4 - ai_text.get_width() // 2, 20))

    def is_game_over(self):
        return (self.player_score >= self.target_score) or (self.ai_score >= self.target_score)

    def check_winner(self):
        if self.player_score >= self.target_score and self.player_score > self.ai_score:
            return "Player"
        if self.ai_score >= self.target_score and self.ai_score > self.player_score:
            return "AI"
        return None

    def reset_for_replay(self, best_of=5):
        best_of = int(best_of)
        if best_of % 2 == 0:
            best_of += 1
        self.target_score = (best_of + 1) // 2
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset(self.width // 2, self.height // 2)
        self.reset_cooldown = self.reset_cooldown_frames
        self.frame_counter = 0
        print(f"[INFO] Restarted game: best_of={best_of}, target_score={self.target_score}")
