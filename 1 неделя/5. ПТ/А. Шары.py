import pygame
import random

pygame.init()
FPS = 60
clock = pygame.time.Clock()

size = width, height = 512, 512
screen = pygame.display.set_mode(size)

balls = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image,
                           pygame.Color((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, balls):
            if self.vx <= 5 and self.vy <= 5:
                self.vy = -self.vy * 1.1
                self.vx = -self.vx * 1.1
            else:
                self.vy = -self.vy
                self.vx = -self.vx
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.add(Ball(20, event.pos[0], event.pos[1]))

    for i, ball in enumerate(balls):
        balls.remove(ball)
        ball.update()
        balls.add(ball)

    screen.fill((0, 0, 0))
    horizontal_borders.draw(screen)
    vertical_borders.draw(screen)
    clock.tick(FPS)

    for ball in balls:
        screen.blit(ball.image, ball.rect)

    pygame.display.flip()

pygame.quit()