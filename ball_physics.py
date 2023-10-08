"""
Done, not touching. If I let myself keep on working on this one I will keep on working on it until I have a full 2d physics engine

Things to finish if I do have a tone of time:
- Different bounces for different edges of floor blocks
- Balls bouncing off each other
- Be able to place blocks and make marble run type things
- Visual effects: Ball changes color on bounce, ball breaks into particles after staying still to long, ball makes ground bounce up and down
"""

import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BOUNCE_RETENTION = 0.6
GRAVITY = pygame.Vector2(0, 0.5)
AIR_RESISTANCE = 0.005

FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falling Shapes")

class Ball(pygame.sprite.Sprite):
    @classmethod
    def random_shape(cls):
        x_range = SCREEN_HEIGHT // 2
        x_velocity_range = 4
        
        center_x = SCREEN_WIDTH // 2
        location = (random.randint(center_x - x_range, center_x + x_range), 0)
        velocity = (random.randint(-x_velocity_range*100, x_velocity_range*100)/100, 0)
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
        
        self.start_time_to_live = 200
        self.start_hide = self.start_time_to_live * 0.5
        self.time_to_live = self.start_time_to_live
        
    @property
    def position(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)
    
    @position.setter
    def position(self, value) -> None:
        self.rect.center = value
        
    def set_random_color(self) -> None:
        pygame.draw.circle(self.image, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (self.radius, self.radius), self.radius)

    def update(self, floors_group: pygame.sprite.Group, other_balls_group: pygame.sprite.Group) -> None:
        floors: list[Floor] = list(floors_group)
        other_balls: list[Ball] = list(other_balls_group)
        
        self.velocity += GRAVITY * self.mass
        self.position += self.velocity

        self.velocity.move_towards_ip((0, 0), AIR_RESISTANCE)
        
        if self.velocity.length() < 2:
            self.time_to_live -= 1
        else:
            self.time_to_live = min(self.start_time_to_live + 10, self.start_time_to_live)
        if self.time_to_live < self.start_hide:
            self.image.set_alpha(255 * (self.time_to_live / self.start_hide))
        if self.time_to_live == 0:
            self.kill()

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.rect.x -= self.velocity.x
            self.velocity.x *= -BOUNCE_RETENTION
                 
        for floor in floors:
            if self.rect.colliderect(floor.rect) and pygame.sprite.collide_mask(self, floor):
                self.rect.y -= self.velocity.y
                                                                         
                angle_radians = math.radians(90 - floor.angle)
                nx = math.cos(angle_radians)
                ny = math.sin(angle_radians)
                self.velocity.reflect_ip((nx, ny))
                    
                self.velocity.y *= (BOUNCE_RETENTION / 2)
          
        for other in other_balls:
            if other is self: continue
            
            # if pygame.sprite.collide_circle(self, other):
            if self.rect.colliderect(other.rect) and pygame.sprite.collide_mask(self, other):
                    nv = (self.position - other.position)
                    if nv.length() > 0:
                        mass_total = self.mass + other.mass
                        self.velocity = self.velocity.reflect(nv.normalize())
                        other.velocity = other.velocity.reflect(nv.normalize())
                        # self.position += nv.normalize() * (1 + other.mass / mass_total)
                    self.position += nv * 0.04
                    
class Floor(pygame.sprite.Sprite):
    def __init__(self, size: pygame.Vector2, location: pygame.Vector2 = (0, 0), angle = 0) -> None:
        super().__init__()
        
        self.angle = angle % 180
        self.mass = float("inf")
        
        self.speed = pygame.Vector2(0, 0)
        
        self.image = pygame.Surface(size)
        self.rect = pygame.rect.Rect(location, pygame.Vector2(location) + size)
        
        self.image.fill(BLACK)
        
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image.set_colorkey((255, 255, 255))
        
    
class Paddle(Floor):
    def __init__(self, size: pygame.Vector2, location: pygame.Vector2 = (0, 0)) -> None:
        super().__init__(size, location) 
        
        color = (0, 75, 214)
        
        self.image_start = self.image
        
        self.image.fill(color)
        
        self.spin_speed = 5
                 
        self.should_move = False
         
    def update(self) -> None:
        
        keys = pygame.key.get_pressed()
                
        if keys[pygame.K_LEFT]:
            self.angle = (self.angle + self.spin_speed) % 180
        if keys[pygame.K_RIGHT]:
            self.angle = (self.angle - self.spin_speed) % 180
            
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
    
    floor_height = SCREEN_HEIGHT * 0.9
    
    floor = Floor((SCREEN_WIDTH, SCREEN_HEIGHT * 0.1), (0, floor_height))
    floors.add(floor)
    
    paddle = Paddle((100, 10))
    floors.add(paddle)

    while running:
        if pygame.event.get(pygame.QUIT):
            running = False
   
        if random.randint(0, 125) == 0:
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