import pygame
pygame.init()

screen = pygame.display.set_mode([1000,1000])

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = false

    screen.fill((255,255,255))

    pygame.draw.circle(screen, (0,0,240), (100,200), 50)

    pygame.display.flip()

pygame.quit()
