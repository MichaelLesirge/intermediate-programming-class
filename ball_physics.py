import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRAVITY = pygame.Vector2(0, 0.5)
BOUNCE_RETENTION = 0.7
AIR_RESISTANCE = 0.005

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Shapes")

class Ball(pygame.sprite.Sprite):
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
        
        self.velocity = pygame.Vector2(velocity) 
        
    @property
    def position(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)
    
    @position.setter
    def position(self, value) -> None:
        self.rect.center = value
        
    def set_random_color(self) -> None:
        pygame.draw.circle(self.image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (self.radius, self.radius), self.radius)

    def on_screen(self):
        return 0 < self.rect.x < SCREEN_WIDTH and 0 < self.rect.y < SCREEN_HEIGHT  
    
    def update(self, floors_group: pygame.sprite.Group, other_balls_group: pygame.sprite.Group) -> None:        
        floors: list[Floor] = list(floors_group)
        other_balls: list[Ball] = list(other_balls_group)
        
        self.velocity.move_towards_ip((0, 0), AIR_RESISTANCE)
        
        self.position += self.velocity

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.velocity.x *= -BOUNCE_RETENTION
                
        for floor in floors:
            
            x, y = self.position
            
            x_hit = floor.rect.left < self.rect.right and self.rect.left < floor.rect.right
            
            if not x_hit: continue
            
            amount_above = floor.rect.top - self.rect.bottom
            
            is_reverse, a_angle = divmod(floor.angle, 90)
            
            b = (floor.rect.right - x) if is_reverse else (x - floor.rect.left)
            a =  math.tan(a_angle) * b
            
            y_bounce = y + a + amount_above  
                        
            top_bounce = y_bounce - self.velocity.y < self.rect.y < y_bounce + self.velocity.y
            bottom_bounce = False
            
            if not (bottom_bounce or top_bounce): continue
                
            self.rect.bottom = floor.rect.top
            angle_radians = math.radians(floor.angle if top_bounce else (180 - floor.angle) % 360)
                
            nx = math.cos(angle_radians)
            ny = math.sin(angle_radians)
            self.velocity.reflect_ip((nx, ny))
            self.velocity.y *= BOUNCE_RETENTION
            self.velocity.move_towards_ip((0, 0), AIR_RESISTANCE)
            
            break
        else:
            self.velocity += GRAVITY
            
        
    
class Floor(pygame.sprite.Sprite):
    def __init__(self, size: pygame.Vector2, location: pygame.Vector2 = (0, 0)) -> None:
        super().__init__()
        
        self.angle = 90
        self.mass = float("inf")
        
        self.speed = pygame.Vector2(0, 0)
        
        self.image_start = pygame.Surface(size)
        self.rect = pygame.rect.Rect(location, pygame.Vector2(location) + size)
        
        self.image_start.fill(BLACK)
        self.image = self.image_start
    
class Paddle(Floor):
    def __init__(self, size: pygame.Vector2, location: pygame.Vector2 = (0, 0)) -> None:
        super().__init__(size, location)
        self.angle = 0
        
        change_size = 5
        color = (0, 75, 214)
        
        self.image.fill(color)
        
        self.spin_speed = change_size
        self.grow_size = change_size
                
        self.image.set_colorkey((0, 0, 0))
        
        self.should_move = False
         
    def update(self) -> None:
        
        keys = pygame.key.get_pressed()
                
        if keys[pygame.K_LEFT]:
            self.angle = (self.angle + self.spin_speed) % 180
        if keys[pygame.K_RIGHT]:
            self.angle = (self.angle - self.spin_speed) % 180
        # if keys[pygame.K_UP]:
        #     self.width = min(self.width + self.grow_size, 100)
        # if keys[pygame.K_DOWN]:
        #     self.width - max(self.grow_size - self.grow_size, 0)
        
        self.image = pygame.transform.rotate(self.image_start, self.angle)
        self.rect = self.image.get_rect()
        
        if self.should_move:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.y = SCREEN_HEIGHT
            self.should_move = pygame.mouse.get_pos() != (0, 0)
                

def main():
    shapes = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True

    floors = pygame.sprite.Group()
    
    floor = Floor((SCREEN_WIDTH, SCREEN_HEIGHT * 0.1), (0, SCREEN_HEIGHT * 0.9))
    floors.add(floor)
    
    paddle = Paddle((100, 10))
    floors.add(paddle)

    while running:
        if pygame.event.get(pygame.QUIT):
            running = False
   
        if random.randint(0, 75) == 0:
            new_shape = Ball.random_shape()
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