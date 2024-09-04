import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame
from pygame.locals import *
from pygame.math import Vector2 as vector 

SCALE=4
WINDOW_WIDTH, WINDOW_HEIGHT = 256*SCALE,192*SCALE
GAME_WIDTH=(256-48)*SCALE
TILE_SIZE = 8*SCALE 
FRAMERATE = 60

