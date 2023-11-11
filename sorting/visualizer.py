import pygame

import algorithms
from util import make_random

pygame.init()

class Config:
    SORTING_ALGORITHMS = [algorithms.bubble_sort, algorithms.insertion_sort, algorithms.selection_sort, algorithms.merge_sort, algorithms.quick_sort]
    
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    
    HEIGHT_MIN, HEIGHT_MAX = 1, SCREEN_HEIGHT - 1

    BASE_FPS = 60
    
    ARRAY_LENGTHS = {10: 1, 25: 2, 100: 5, 250: 10, 500: 10, 1000: 10}
    
    # NUM_RANGE = (0, 10000)
    NUM_RANGE = None
    
    WAIT_AT_END = 0.5
    
    BACKGROUND_COLOR = (0, 0, 0)
    DEFAULT_BLOCK_COLOR = (255, 255, 255)
    
    READ_BLOCK_COLOR = "grey"
    PAST_WRITE_BLOCK_COLOR = "aquamarine2"
    WRITE_BLOCK_COLOR = "green"
    
    TEXT_COLOR = ()
    
    FPS_CHANGE = 0.5

class SortDisplayArray(list):
    def __init__(self, array: list[int], update_func = lambda s: None):
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
                
        self.rect = pygame.Rect(0, 0, (self.width_unit), Config.HEIGHT_MAX)
    
    def get_rect(self, index, value):
        # cant use setdefault since it would always still makes the new rect
        
        # if value not in self.rect_key: self.rect_key[value] = self.make_rect_value(index, value)
        self.rect.x = (self.width_unit * index)
        self.rect.y = Config.SCREEN_HEIGHT - (Config.HEIGHT_MIN + self.height_unit * value)
        return self.rect
    
    def draw_all(self, screen: pygame.Surface) -> None:
        highlighted_indexes = {value: key for key, value in self.marks.items()}
        for index, value in enumerate(self):
            pygame.draw.rect(screen, highlighted_indexes.get(index, Config.DEFAULT_BLOCK_COLOR), self.get_rect(index, value))
        
    def __getitem__(self, index):
        self.reads += 1
        
        self.marks[Config.READ_BLOCK_COLOR] = index
        self.update_func(self)
        
        return super().__getitem__(index)

    def __setitem__(self, index, value): 
        if isinstance(index, slice):
            for i, slice_i in enumerate(range(index.start or 0, index.stop or len(self), index.step or 1)):
                self[slice_i] = value[i]
        else:
            self.writes += 1
            
            # if Config.MAX_DURATION != 0: threading.Thread(target=self.beep, args=(value,), kwargs={}).start()
            
            # self.marks[Config.PAST_WRITE_BLOCK_COLOR] = self.marks.get(Config.WRITE_BLOCK_COLOR, -1)
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

    print("Controls")
    print("Speed Up: Up Arrow")
    print("Slow Down: Down Arrow")
    print("Skip: Space")
    print()
    
    for length, fps_adjuster_default in Config.ARRAY_LENGTHS.items():
        
        fps_adjuster_default_text = f" Default speed is {round(fps_adjuster_default, 2)}x."
        print(f"Sorting demo for {length} element array.{'' if fps_adjuster_default == 1 else fps_adjuster_default_text}")
                
        for sorter in Config.SORTING_ALGORITHMS:
            fps_adjuster = fps_adjuster_default
                                
            def update_screen(display_array: SortDisplayArray):
                nonlocal fps_adjuster
                                                                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: exit(pygame.quit())
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_DOWN]: fps_adjuster = round(max(fps_adjuster - Config.FPS_CHANGE, 0), 2)
                        if event.key in [pygame.K_UP]: fps_adjuster = round(min(fps_adjuster + Config.FPS_CHANGE, 20), 2)
                        if event.key in [pygame.K_RIGHT, pygame.K_SPACE]: fps_adjuster = float("inf")
                        
                if fps_adjuster == float("inf"): return

                screen.fill(Config.BACKGROUND_COLOR)        
                display_array.draw_all(screen)
                
                fps = int(Config.BASE_FPS * fps_adjuster) if fps_adjuster else 1
                                
                fps_data =  f"{fps} FPS" + ("" if fps_adjuster in (0, 1) else f" ({fps_adjuster}x speed)") + ("" if fps - clock.get_fps() < 100 else f". Real FPS {int(round(clock.get_fps(), -2))}") + "."
                text = font.render(f"{sorter.__name__} - {display_array.reads} reads, {display_array.writes} writes. {fps_data}", True, (200, 200, 250))
                text_rect = text.get_rect()
                
                screen.blit(text, text_rect)
                
                pygame.display.flip()
                
                clock.tick(fps)
                            
            array = make_random(length, Config.NUM_RANGE) 
            display_array = SortDisplayArray(array, update_screen)
                    
            sorter(display_array)
                            
            update_screen(display_array)
            
            print(f"{sorter.__name__}:\t{display_array.reads} reads,\t{display_array.writes} writes.")
            
            if fps_adjuster != float("inf"): pygame.time.delay(int(Config.WAIT_AT_END * 1000)) 
        
        print()
        
    pygame.quit()

if __name__ == "__main__":
    main()
    
    