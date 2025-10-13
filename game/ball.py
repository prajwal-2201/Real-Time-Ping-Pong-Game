import pygame
import random
import math

class Ball:
    """
    Ball uses center coordinates (self.x, self.y as floats) for smooth movement.
    width/height are integers for drawing and collisions.
    """

    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.width = int(width)
        self.height = int(height)
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)

        self.original_x = float(x)
        self.original_y = float(y)
        self.x = float(x)
        self.y = float(y)

        self.speed = 5.0
        self._randomize_velocity()

    def _randomize_velocity(self):
        angle = random.uniform(-0.4, 0.4)  # bias mostly horizontal
        direction = random.choice([-1, 1])
        self.velocity_x = direction * self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)

    def move(self):
        # move using float positions
        self.x += self.velocity_x
        self.y += self.velocity_y

        # bounce off top/bottom borders (keep inside)
        if self.top() <= 0:
            self.y = self.height / 2
            self.velocity_y = -self.velocity_y
            return "wall"
        if self.bottom() >= self.screen_height:
            self.y = self.screen_height - self.height / 2
            self.velocity_y = -self.velocity_y
            return "wall"
        return None

    def check_collision(self, player, ai):
        """
        Returns:
          "player" if collided with player paddle,
          "ai" if collided with ai paddle,
          None otherwise.
        This uses rect collision and pushes ball outside the paddle to avoid sticking.
        """
        ball_rect = self.rect()
        # player collision
        if ball_rect.colliderect(player.rect()):
            # push ball outside of paddle depending on side
            # if coming from left side, put it to the right of paddle
            if self.velocity_x < 0:
                self.x = player.x + player.width + self.width / 2
            else:
                self.x = player.x - self.width / 2
            self._bounce_off_paddle(player)
            return "player"

        # ai collision
        if ball_rect.colliderect(ai.rect()):
            if self.velocity_x > 0:
                self.x = ai.x - self.width / 2
            else:
                self.x = ai.x + ai.width + self.width / 2
            self._bounce_off_paddle(ai)
            return "ai"

        # Extra check for high speed: if ball jumped past paddle in one frame,
        # check approximate crossing by projecting previous position.
        # We can compute previous center from velocity and see if line intersects paddle rect horizontally.
        prev_x = self.x - self.velocity_x
        # If prev_x was left of player and current x is right of player, consider collision.
        # This is a simple continuous check to catch fast passes.
        if self.velocity_x > 0:
            # moving right: check crossing ai paddle vertical slab
            slab_left = ai.x
            slab_right = ai.x + ai.width
            if prev_x < slab_left and self.x >= slab_left:
                # check y overlap with ai paddle
                if (self.y + self.height/2) >= ai.y and (self.y - self.height/2) <= (ai.y + ai.height):
                    self.x = ai.x - self.width / 2
                    self._bounce_off_paddle(ai)
                    return "ai"
        else:
            # moving left: check crossing player paddle vertical slab
            slab_left = player.x
            slab_right = player.x + player.width
            if prev_x > slab_right and self.x <= slab_right:
                if (self.y + self.height/2) >= player.y and (self.y - self.height/2) <= (player.y + player.height):
                    self.x = player.x + player.width + self.width / 2
                    self._bounce_off_paddle(player)
                    return "player"

        return None

    def _bounce_off_paddle(self, paddle):
        """
        Adjust velocity based on where the ball hits the paddle;
        tilt vertical speed based on offset from paddle center.
        """
        paddle_center = paddle.y + paddle.height / 2
        offset = (self.y - paddle_center) / (paddle.height / 2)
        offset = max(-1.0, min(1.0, offset))

        # slightly increase speed to make game progressively harder
        self.speed *= 1.02
        # flip horizontal direction, keep sign consistent
        self.velocity_x = -math.copysign(self.speed, self.velocity_x)
        # tilt vertical velocity
        self.velocity_y = offset * (self.speed * 0.6)
        if abs(self.velocity_y) < 0.5:
            self.velocity_y = math.copysign(0.5, self.velocity_y)

    def reset(self, center_x=None, center_y=None):
        if center_x is None:
            center_x = self.original_x
        if center_y is None:
            center_y = self.original_y
        self.x = float(center_x)
        self.y = float(center_y)
        self.speed = 5.0
        self._randomize_velocity()

    def rect(self):
        left = int(round(self.x - self.width / 2))
        top = int(round(self.y - self.height / 2))
        return pygame.Rect(left, top, int(self.width), int(self.height))

    # helpers
    def top(self):
        return self.y - self.height / 2

    def bottom(self):
        return self.y + self.height / 2

    def left(self):
        return self.x - self.width / 2

    def right(self):
        return self.x + self.width / 2
