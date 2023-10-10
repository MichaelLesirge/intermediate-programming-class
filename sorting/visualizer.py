import pygame

from util import make_random
import algorithms

import threading

"""
Bubble, Insertion, Selection, Merge, and Quick Sort
Option of shuffled mode and random number mode
Beeps based on element size
Display name of sorting, (comparisons, swaps) and (reads, writes)
highlight relevant indexes

graph time of sorting for different array sizes at end
"""

pygame.init()

class Config:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    FPS = 60
    
    ARRAY_LENGTH = 100
    NUM_RANGE = None
    
    BACKGROUND_COLOR = (0, 0, 0)
    DEFAULT_BLOCK_COLOR = (255, 255, 255)
    
"""TODO at some point make this work async from actual sorting"""
class SortDisplayArray(list):
    
    def __init__(self, array: list):
        super().__init__(array)        
        self.reads = 0
        self.writes = 0
        
        self.height_unit = max(array) / Config.SCREEN_HEIGHT
        
        self.width_unit = len(array) / Config.SCREEN_WIDTH
        
        # TODO keep track of updates and only draw changes
        # self.updates = []
        
        self.rect_key: dict[int, pygame.Rect] = {value: self.make_value_rect(value, index) for index, value in enumerate(self)}
    
    def make_value_rect(self, index: int, value: int) -> pygame.Rect:
        return pygame.Rect(self.width_unit * index, self.height_unit * value, self.width_unit, self.height_unit * value)
    
    def draw_all(self, screen: pygame.Surface, highlighted_rect: dict[int: pygame.Color] = {}) -> None:
        for index, value in enumerate(self):
            pygame.draw.rect(screen, highlighted_rect.get(index, Config.DEFAULT_BLOCK_COLOR), self.rect_key[value])
    
    def __getitem__(self, index):
        self.reads += 1
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        self.writes += 1
        self.rect_key[value] = self.make_value_rect(index, value)
        return super().__setitem__(index, value)
    
    def __str__(self) -> str:
        return f"<{super().__str__()}, reads={self.reads}, writes={self.writes}>"
        

def main() -> None:    
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("Falling Shapes")
    
    clock = pygame.time.Clock()
    
    sorting_algorithms = [algorithms.bubble_sort]
    
    for sorter in sorting_algorithms:
         
        array = SortDisplayArray(make_random(Config.ARRAY_LENGTH, Config.NUM_RANGE))
                 
        for sorter_state in sorter(array, yield_state=True):
            if pygame.event.get(pygame.QUIT):
                return pygame.quit()
                        
            screen.fill(Config.BACKGROUND_COLOR)
            array.draw_all(screen, sorter_state)
        
            clock.tick(Config.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()