import pygame
import time
import math
GRASS=pygame.image.load("assets/grass.jpg")
TRACK=pygame.image.load("assets/track.png")
TRACK_BORDER=pygame.image.load("assets/track-border.png")
FINISH=pygame.image.load("assets/finish.png")

CARS=[pygame.image.load(f'assets/img{i+1}.png')  for i in range(13)]
WIDTH,HEIGHT=TRACK.get_width(),TRACK.get_height()
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
FPS=60
pygame.display.set_caption("hello world")
run = True
clock=pygame.time.Clock()
while run:
    clock.tick(FPS) 
    WIN.blit(GRASS,(0,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            break
pygame.quit()