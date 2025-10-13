import pygame

class Paddle:
    """
    Paddle uses top-left coordinates for .x and .y (integers).
    """

    def __init__(self, x, y, width, height, speed=7):
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.speed = int(speed)

    def move(self, dy, screen_height):
        # dy positive moves down
        self.y += int(dy)
        # clamp to screen
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.width), int(self.height))

    def auto_track(self, ball, screen_height):
        # aim to center paddle on ball's center with a small deadzone
        paddle_center = self.y + self.height / 2
        if ball.y < paddle_center - 6:
            self.move(-self.speed, screen_height)
        elif ball.y > paddle_center + 6:
            self.move(self.speed, screen_height)
