from flappybird import Game, Pipe
import pygame

pygame.init()
pygame.font.init()
pygame.display.set_caption('FLAPPY-BIRD')
font = pygame.font.Font(None, 50)


def main():
    frames, stop = 0, False
    clock = pygame.time.Clock()
    game = Game()
    # Game loop.
    while not stop:
        if not game.lost:
            for pipe in game.pipes:
                pipe.been_passed(game.bird, game)
                if pipe.offscreen():
                    game.pipes.pop(0)
                if pipe.is_hit(game.bird):
                    game.stop()
                    game.lost = True
            if not (frames % 110):
                game.pipes.append(Pipe())
        game.update()
        game.draw()
        game.screen.blit(font.render('{0}'.format(game.score), 1, (0, 100, 200)), (game.width/2, 20))
        frames += 1
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.lost:
                        game.restart()
                    game.bird.up()
            if event.type == pygame.QUIT:
                stop = True

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
