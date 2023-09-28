import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BOUNCE_RETENTION = 1
GRAVITY = 1

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Shapes")

class Drop(pygame.sprite.Sprite):
    @classmethod
    def random_shape(cls):
        # location = (random.randint(0, SCREEN_WIDTH), 0)
        center_x = SCREEN_WIDTH // 2
        location = (random.randint(center_x - 10, center_x + 10), 0)
        velocity = (random.randint(-5, 5), 0)
        size = random.randint(20, 50)
        return cls(size, location, velocity) 
    
    def __init__(self, radius: float, location: pygame.Vector2, velocity: pygame.Vector2):
        super().__init__()
        self.radius = radius
        
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(center = location)
        self.set_random_color()
        
        self.rect.center = location
        
        area = math.pi * self.radius ** 2
        density = 0.0001
        self.mass = area * density
        
        self.start_time_to_live = 50
        
        self.time_to_live = self.start_time_to_live
        
        self.velocity = pygame.Vector2(velocity) 
        
    def set_random_color(self):
        pygame.draw.circle(self.image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (self.radius, self.radius), self.radius)

    def update(self, floors: pygame.sprite.Group, other_balls: pygame.sprite.Group):
        floors: list[Floor] = list(floors)
        
        # https://www.youtube.com/watch?v=Ge1DbXkyMKo&ab_channel=griffpatch
        self.velocity.y += GRAVITY
                
        self.rect.center += self.velocity
        
        collide_floor = self.rect.collidelist(floors)
        
        if collide_floor != -1:
            self.rect.y -= self.velocity.y 
            self.velocity.y *= -0.6
            
        
    
class Floor(pygame.sprite.Sprite):
    def __init__(self, size: pygame.Vector2, location: pygame.Vector2 = (0, 0), follow_provider = None) -> None:
        super().__init__()
        
        self.rotation = 0
        
        self.location_func = follow_provider
        
        self.image = pygame.Surface(size)
        pygame.rect.Rect(location, pygame.Vector2(location) + size)
        self.rect = self.image.get_rect()
        
        if not follow_provider: self.rect.topleft = location
        self.image.fill(BLACK)
    
    def update(self) -> None:
        if self.location_func: self.rect.center = self.location_func()
        # self.rect.clamp_ip((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    shapes = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True

    floors = pygame.sprite.Group()
    
    floor = Floor((SCREEN_WIDTH, SCREEN_HEIGHT * 0.1), (0, SCREEN_HEIGHT * 0.9))
    floors.add(floor)
    
    paddle = Floor((100, 10), follow_provider=pygame.mouse.get_pos)
    floors.add(paddle)

    # new_shape = Drop.random_shape()
    # shapes.add(new_shape)
        
    while running:
        if pygame.event.get(pygame.QUIT):
            running = False
   
        if random.randint(0, 75) == 0:
            new_shape = Drop.random_shape()
            shapes.add(new_shape)
        
        shapes.update(floors, shapes)
        floors.update()
        
        screen.fill(WHITE)
        
        shapes.draw(screen)
        floors.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


    pygame.quit()

if __name__ == "__main__":
    main()