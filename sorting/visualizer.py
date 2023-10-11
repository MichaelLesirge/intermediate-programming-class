import pygame

import algorithms
from util import make_random

pygame.init()

class Config:
    SORTING_ALGORITHMS = [algorithms.bubble_sort, algorithms.insertion_sort, algorithms.selection_sort, algorithms.merge_sort]
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    
    HEIGHT_MIN, HEIGHT_MAX = 1, SCREEN_HEIGHT - 1

    BASE_FPS = 60
    
    ARRAY_LENGTH = 100
    NUM_RANGE = None
    
    BACKGROUND_COLOR = (0, 0, 0)
    DEFAULT_BLOCK_COLOR = (255, 255, 255)
    
    READ_BLOCK_COLOR = "grey"
    WRITE_BLOCK_COLOR = "green"
    
    TEXT_COLOR = ()
    
    FPS_CHANGE = 0.5

# TODO id all values in array (inherit from int) and then always have smooth mode and go back to storing rects in dict  
class SortDisplayArray(list):
    def __init__(self, array: list, update_func = lambda s: None):
        super().__init__(array)        
        self.reads = 0
        self.writes = 0
                
        self.update_func = update_func
        
        # self.height_unit = Config.SCREEN_HEIGHT / max(array)
        self.height_unit = (Config.HEIGHT_MAX - Config.HEIGHT_MIN) / max(array)
        
        self.width_unit = Config.SCREEN_WIDTH / len(array)
         
        # TODO keep track of updates and only draw changes
        # self.updates = []
        
        self.marks: dict[int, pygame.Color] = {}    
            
        self.rect_key: dict[int, pygame.Rect] = {value: self.make_value_rect(value, index) for index, value in enumerate(self)}
    
    def make_value_rect(self, index: int, value: int) -> pygame.Rect:
        # height = Config.SCREEN_HEIGHT - value * self.height_unit
        height = Config.HEIGHT_MAX - value * self.height_unit
        return pygame.Rect((self.width_unit * index), height, self.width_unit, Config.SCREEN_HEIGHT)
    
    def draw_all(self, screen: pygame.Surface) -> None:
        highlighted_indexes = {value: key for key, value in self.marks.items()}
        for index, value in enumerate(self):
            pygame.draw.rect(screen, highlighted_indexes.get(index, Config.DEFAULT_BLOCK_COLOR), self.make_value_rect(index, value))
        
    def __getitem__(self, index):
        self.reads += 1
        
        self.marks[Config.READ_BLOCK_COLOR] = index
        self.update_func(self)
        
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        self.writes += 1
         
        # if Config.MAX_DURATION != 0: threading.Thread(target=self.beep, args=(value,), kwargs={}).start()
         
        self.marks[Config.WRITE_BLOCK_COLOR] = index
        self.update_func(self)
        
        return super().__setitem__(index, value)
    
    def __str__(self) -> str:
        return f"<{super().__str__()}, reads={self.reads}, writes={self.writes}>"
        

def main() -> None:    
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("Sorting")
    
    clock = pygame.time.Clock()
        
    font = pygame.font.Font('sorting/font.ttf', 16)
    
     
    for sorter in Config.SORTING_ALGORITHMS:
        fps_adjuster = 1
                 
        def update_screen(display_array):
            nonlocal fps_adjuster
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit(pygame.quit())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN: fps_adjuster = round(max(fps_adjuster - Config.FPS_CHANGE, 0), 2)
                    if event.key == pygame.K_UP: fps_adjuster = round(min(fps_adjuster + Config.FPS_CHANGE, 20), 2)
                    if event.key == pygame.K_RIGHT: fps_adjuster = float("inf")
                    
            if fps_adjuster == float("inf"): return

            screen.fill(Config.BACKGROUND_COLOR)        
            display_array.draw_all(screen)
            
            fps = int(Config.BASE_FPS * fps_adjuster) if fps_adjuster else 1
            
            fps_data =  f" {fps} FPS" + ('' if fps_adjuster in (0, 1) else f" ({fps_adjuster}x speed)")
            text = font.render(f"{sorter.__name__} - {display_array.reads} reads, {display_array.writes} writes - {fps_data}", True, (200, 200, 250))
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
    
    