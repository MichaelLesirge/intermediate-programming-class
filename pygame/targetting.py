import pygame
import random
import math

pygame.init()

class Config:
    NAME = "Targeting"
    
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    GRAVITY = pygame.Vector2(0, -9.8)
    AIR_RESISTANCE = 0.005

    FPS = 60
    BACKGROUND_COLOR = (255, 255, 255)
    
    METER = 50

screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
pygame.display.set_caption(Config.NAME)

class Target(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        
        self.width = 10
        self.color = (100, 0, 0)
        
        self.image = pygame.Surface((self.width, self.width))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
    
    def update(self) -> None:
        x, y = pygame.mouse.get_pos()
        radius = self.width // 2
        self.rect = pygame.draw.circle(self.image, self.color, (x - radius, y - radius), radius)
        
        
class TennisBall(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.Surface()
        self.rect = self.image.get_rect()
    
    def update(self) -> None:
        pass

def main():
    running = True
    
    show_distance_line = True
    
    clock = pygame.time.Clock()
    
    sprites = pygame.sprite.Group()
    
    target = Target()
    
    sprites.add(target)
    
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_SPACE:
                            running = False

        screen.fill(Config.BACKGROUND_COLOR)
        sprites.update()
        sprites.draw(screen)
         
        pygame.display.flip()

        clock.tick(Config.FPS)


    pygame.quit()

if __name__ == "__main__":
    main()