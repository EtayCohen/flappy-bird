import pygame, random

pygame.init()

HEIGHT = 512
WIDTH = 512
PIPES_SPACING = 100
PIPES_WIDTH = 50
GRAVITY = 0.65
LIFT = 13.5
OFFSET = 100


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

    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (255, 0, 0), (self.x, int(self.y)), 20)

    def update(self):
        if self.y < HEIGHT:
            self.velocity += self.gravity
            self.y += self.velocity

    def is_hit(self):
        return not 0 < self.y < HEIGHT


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
            if self.x + PIPES_WIDTH > bird.x > self.x:
                return True
        return False

    def stop(self):
        self.velocity = 0


def main():
    frames, stop = 0, False
    clock = pygame.time.Clock()
    game = Game()
    # Game loop.
    while not stop:
        if not game.lost:
            for pipe in game.pipes:
                if pipe.is_hit(game.bird) or game.bird.is_hit():
                    game.stop()
                    game.lost = True
            if not (frames % 110):
                game.pipes.append(Pipe())
                if len(game.pipes) > 2:
                    game.pipes.pop(0)
        game.update()
        game.draw()
        frames += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.lost:
                        game.restart()
                    game.bird.velocity -= LIFT
            if event.type == pygame.QUIT:
                stop = True

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
