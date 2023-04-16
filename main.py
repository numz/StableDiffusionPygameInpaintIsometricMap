import pygame
from simulation.game import Game

def main():
    pygame.init()
    game = Game()
    game.load_map()
    while game.running:
        game.handle_events()
        game.update()
        game.draw()
    pygame.quit()


if __name__ == "__main__":
    main()
