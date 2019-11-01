import pygame, random

pygame.init()

HEIGHT = 500
WIDTH = 500
PIPES_SPACING = 100
PIPES_WIDTH = 50
LIFT = 10
OFFSET = 100


class Game:
    def __init__(self):
        self.width, self.height = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((255, 255, 255))
        self.bird = Bird()
        self.pipes = []

    def draw(self):
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)

    def update(self):
        self.bird.update()
        for pipe in self.pipes:
            pipe.update()


class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT/2
        self.velocity = 0
        self.gravity = 0.8

    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (self.x, int(self.y)), 20)

    def update(self):
        if self.velocity < 20:
            self.velocity += self.gravity
        self.y += self.velocity
        self.y %= HEIGHT


class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.top = random.randint(OFFSET, HEIGHT - OFFSET)
        self.bottom = HEIGHT - (self.top + PIPES_SPACING)
        self.velocity = 3

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, PIPES_WIDTH, self.top))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.top + PIPES_SPACING, PIPES_WIDTH, self.bottom))

    def update(self):
        self.x -= self.velocity

    def is_hit(self, bird):
        if bird.y > self.top + PIPES_SPACING or bird.y < self.top:
            if self.x + 50 > bird.x > self.x:
                print("HIT")


def main():
    frames = 0
    clock = pygame.time.Clock()
    game = Game()
    # Game loop.
    while True:
        for pipe in game.pipes:
            pipe.is_hit(game.bird)
        if not (frames % 100):
            game.pipes.append(Pipe())
            if len(game.pipes) > 2:
                game.pipes.pop(0)
        # Game update
        game.update()
        # Game draw
        game.draw()
        frames += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.bird.velocity -= LIFT
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
