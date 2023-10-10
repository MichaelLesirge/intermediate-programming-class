import pygame

from util import make_random
import algorithms

sorting_algorithms = {algorithms.bubble_sort: 2, algorithms.insertion_sort: 1, algorithms.selection_sort: 1}

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
    
    HEIGHT_MIN, HEIGHT_MAX = 1, SCREEN_HEIGHT - 1

    FPS = 60
    
    ARRAY_LENGTH = 100
    NUM_RANGE = None
    
    BACKGROUND_COLOR = (0, 0, 0)
    DEFAULT_BLOCK_COLOR = (255, 255, 255)

# TODO id all values in array (inherit from int) and then always have smooth mode and go back to storing rects in dict  
class SortDisplayArray(list):
    def __init__(self, array: list, update_func = lambda s: None):
        super().__init__(array)        
        self.reads = 0
        self.writes = 0
                
        self.update_func = update_func
        
        # self.height_unit = Config.SCREEN_HEIGHT // max(array)
        self.height_unit = (Config.HEIGHT_MAX - Config.HEIGHT_MIN) // max(array)
        
        self.width_unit = Config.SCREEN_WIDTH // len(array)
        
        # TODO keep track of updates and only draw changes
        # self.updates = []
        
        self.marks: dict[int, pygame.Color] = {}    
            
        self.rect_key: dict[int, pygame.Rect] = {value: self.make_value_rect(value, index) for index, value in enumerate(self)}
    
    def make_value_rect(self, index: int, value: int) -> pygame.Rect:
        height = (self.height_unit * value) + Config.HEIGHT_MIN
        return pygame.Rect(Config.SCREEN_WIDTH - (self.width_unit * (index + 1)), height, self.width_unit, Config.SCREEN_HEIGHT)
    
    def draw_all(self, screen: pygame.Surface) -> None:
        highlighted_indexes = {value: key for key, value in self.marks.items()}
        for index, value in enumerate(self):
            pygame.draw.rect(screen, highlighted_indexes.get(index, Config.DEFAULT_BLOCK_COLOR), self.make_value_rect(index, value))
    
    def __getitem__(self, index):
        self.reads += 1
        
        # self.marks["red"] = index
        # self.update_func(self)
        
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        self.writes += 1
        
        self.marks["green"] = index
        self.update_func(self)
        
        return super().__setitem__(index, value)
    
    def __str__(self) -> str:
        return f"<{super().__str__()}, reads={self.reads}, writes={self.writes}>"
        

def main() -> None:    
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("Falling Shapes")
    
    clock = pygame.time.Clock()
        
    font = pygame.font.Font('sorting/font.ttf', 16)
     
    for sorter, fps_adjuster in sorting_algorithms.items():  
        def update_screen(display_array):
            if pygame.event.get(pygame.QUIT):
                exit(pygame.quit())

            screen.fill(Config.BACKGROUND_COLOR)        
            display_array.draw_all(screen)
            
            fps = int(Config.FPS * fps_adjuster)
            
            speed_multiplayer = f" ({fps_adjuster}x speed)"
            text = font.render(f"{sorter.__name__} - {display_array.reads} reads, {display_array.writes} writes. {fps} FPS{'' if fps_adjuster == 1 else speed_multiplayer}", True, "white")
            text_rect = text.get_rect()
            
            screen.blit(text, text_rect)
            
            pygame.display.flip()
            
            clock.tick(fps)
         
        array = make_random(Config.ARRAY_LENGTH, Config.NUM_RANGE) 
        display_array = SortDisplayArray(array, update_screen)
                
        sorter(display_array)
                        
        update_screen(display_array)
        
    pygame.quit()

if __name__ == "__main__":
    main()