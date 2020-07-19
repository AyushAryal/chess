import pygame

height=500
width=500
win=pygame.display.set_mode((heigth,width))
pygame.display.set_caption("Chess")

run=True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run=False

        pygame.display.update()

pygame.quit()

