import pygame
pygame.init()

import screens

def main():
    height = 800
    width = 800
    window = pygame.display.set_mode((height, width))
    pygame.display.set_caption("PyChess")

    new_screen = screens.start_screen
    while (new_screen := new_screen(window)) != True:
        ...


if __name__ == '__main__':
    main()
