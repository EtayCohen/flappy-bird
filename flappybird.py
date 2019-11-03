import pygame, random

pygame.init()
pygame.font.init()
pygame.display.set_caption('FLAPPY-BIRD')
font = pygame.font.Font(None, 50)
HEIGHT = 480
WIDTH = 640
PIPES_SPACING = 120
PIPES_WIDTH = 50
GRAVITY = 0.6
LIFT = - 12
OFFSET = 50
PIPE_VELOCITY = 3
SIZE = 20


class Game:
    def __init__(self):
        self.width, self.height = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))
        self.bird = Bird()
        self.pipes = []
        self.lost = False
        self.score = 0

    def draw(self):
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)

    def update(self):
        self.bird.update()
        for pipe in self.pipes:
            pipe.update()

    def restart(self):
        self.screen.fill((255, 255, 255))
        self.bird = Bird()
        self.pipes = []
        self.lost = False
        self.score = 0

    def stop(self):
        for pipe in self.pipes:
            pipe.stop()


class Bird:
    def __init__(self):
        self.x = WIDTH//4
        self.y = HEIGHT/2
        self.velocity = 0
        self.gravity = GRAVITY
        self.score = 0
        self.fitness = 0

    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (250, 250, 0), (self.x, int(self.y)), SIZE)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y >= HEIGHT - 10:
            self.y = HEIGHT - 10/2
            self.velocity = 0

        if self.y <= 10:
            self.y = 10
            self.velocity = 0

    def up(self):
        self.velocity += LIFT


class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.top = random.randint(OFFSET, HEIGHT - OFFSET - PIPES_SPACING)
        self.bottom = HEIGHT - (self.top + PIPES_SPACING)
        self.velocity = PIPE_VELOCITY
        self.passed = False

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, PIPES_WIDTH, self.top))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.top + PIPES_SPACING, PIPES_WIDTH, self.bottom))

    def update(self):
        self.x -= self.velocity

    def is_hit(self, bird):
        if bird.y > self.top + PIPES_SPACING - SIZE or bird.y < self.top + 20:
            if self.x + PIPES_WIDTH > bird.x > self.x - SIZE:
                return True
        return False

    def stop(self):
        self.velocity = 0

    def been_passed(self, bird, game):
        if not self.passed and (self.x + PIPES_WIDTH + SIZE < bird.x):
            self.passed = True
            game.score += 1

    def offscreen(self):
        return self.x < - PIPES_WIDTH


if __name__ == '__main__':
    pass
