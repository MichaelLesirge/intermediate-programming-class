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

screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
pygame.display.set_caption(Config.NAME)

class Sprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
    
    def update(self) -> None:
        self.image = pygame.Surface()
        self.rect = self.image.get_rect()

def main():
    running = True
    
    clock = pygame.time.Clock()
    
    balls = pygame.sprite.Group()
    balls.add()
    
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
            
        pygame.display.flip()

        clock.tick(Config.FPS)


    pygame.quit()

if __name__ == "__main__":
    main()