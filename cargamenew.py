import pygame
import time
import math
GRASS=pygame.image.load("assets/grass.png")
TRACK=pygame.image.load("assets/track.png")
TRACK_BORDER=pygame.image.load("assets/track-border.png")
FINISH=pygame.image.load("assets/finish.png")

CARS=[pygame.image.load(f'assets/img{i+1}.png') i for i in range(13)]
WIDTH,HEIGHT=TRACK.get_width(),TRACK.get_height()
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
WIN.set_caption("hello world")