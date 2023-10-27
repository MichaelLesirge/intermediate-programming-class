# Math and code for this done by much smarter friend, I only cleaned it up

import pygame
import math
import random
import enum

UNIT = 50

class PhysicsConstants:
    GRAVITY = 9.81 * UNIT
   
class AimTypes(enum.Enum):
    AIMED = enum.auto()
    MANUAL = enum.auto()
   
class Settings:
    FPS = 1000
    
    SCREEN_WIDTH, SCREEN_HEIGHT = 20 * UNIT, 15 * UNIT

    AIM_TYPE = AimTypes.AIMED
    DRAW_GRID = True
    
    BACKGROUND = (255, 255, 255)
    
    LINE_COLOR = (100, 100, 100)
    
    
    NUM_OF_TARGETS = 0
 
class Target(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SIZE = 0.5 * UNIT 
    
    def __init__(self, location):
        super().__init__()
        self.x, self.y = location
                        
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.rect = pygame.Rect(self.x, self.y, self.SIZE, self.SIZE)

    def update(self, bullets):
        hits = pygame.sprite.spritecollide(self, bullets, dokill=True)
        # if hits: self.kill()

class Bullet(pygame.sprite.Sprite):
    COLOR = (0, 100, 255)
    RADIUS = 0.1 * UNIT
    
    def __init__(self, location, velocity, angle):
        super().__init__()
        self.time = 0
        self.init_x, self.init_y = location
        self.x, self.y = self.init_x, self.init_y
        self.init_v = velocity
        
        self.angle = angle
                
        self.image = pygame.Surface((self.RADIUS*2, self.RADIUS*2))
        self.rect = self.image.get_rect()

    def update(self):
        self.time += 1/Settings.FPS
        self.x = self.init_x+self.init_v*self.time*math.cos(self.angle)
        self.y = self.init_y+self.init_v*self.time * math.sin(self.angle)+(PhysicsConstants.GRAVITY/2*pow(self.time, 2))
         
        pygame.draw.circle(self.image, self.COLOR, (int(self.x), int(self.y)), int(self.RADIUS), 2)


class Shooter(pygame.sprite.Sprite):
    COLOR = (0, 0, 0)
    RADIUS = 0.5 * UNIT
    
    def __init__(self, location):
        super().__init__()
        
        self.x, self.y = location
            
        self.image = pygame.Surface((self.RADIUS * 2, self.RADIUS * 2), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))
           
        pygame.draw.circle(self.image, self.COLOR, (self.RADIUS, self.RADIUS), self.RADIUS, 3)  
    
    def shoot(self, target_x, target_y, aim_type: AimTypes = AimTypes.AIMED, velocity=400):
        x = target_x - self.x
        y = target_y - self.y

        match aim_type:
            case AimTypes.MANUAL:
                angle = math.atan(y/x)
                if target_x-self.x < 0:
                    angle += math.pi
                    
            case AimTypes.AIMED:
                
                a = PhysicsConstants.GRAVITY*x*x*y/velocity/velocity+x*x
                b = PhysicsConstants.GRAVITY*PhysicsConstants.GRAVITY*pow(x/velocity, 4)
                c = x*x+y*y
                
                if c == 0:
                    angle = -math.pi/2
                else:
                    cos = pow((a+pow(pow(a, 2)-b*c, 1/2))/(2*c), 1/2)
                    if x < 0:
                        cos *= -1
                    try:
                        # angle is negative of reality because pygame has up/down switched
                        angle = math.acos(cos)
                        if x == 0:
                            if y < 0:
                                if y < velocity*velocity/2/PhysicsConstants.GRAVITY:
                                    return
                                angle *= -1
                        elif cos*(y-PhysicsConstants.GRAVITY*x*x/2/velocity/velocity/cos/cos)/x < 0:
                            angle *= -1
                    except TypeError:
                        return

        return Bullet((self.x, self.y), velocity, angle)

def main() -> None:
    width, height = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    shooters = pygame.sprite.Group()

    def random_pos() -> tuple[int, int]:
        return random.randrange(UNIT, width, UNIT), random.randrange(UNIT, width, UNIT)
        
    shooters.add(Shooter(random_pos()))

    bullets = pygame.sprite.Group()
    targets = pygame.sprite.Group()

    for i in range(Settings.NUM_OF_TARGETS):
        target = Target(random_pos())
        targets.add(target)

    going = True

    while going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                shooters.add(Shooter(pygame.mouse.get_pos()))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                x, y = pygame.mouse.get_pos()
                for shooter in shooters:
                    bullets.add(shooter.shoot(x, y, Settings.AIM_TYPE, velocity = 400))

        bullets.update()
        targets.update(bullets)
        shooters.update()
        
        screen.fill(Settings.BACKGROUND)
        if Settings.DRAW_GRID:
            for x in range(UNIT, Settings.SCREEN_WIDTH, UNIT):
                pygame.draw.line(screen, Settings.LINE_COLOR, (x, 0), (x, Settings.SCREEN_HEIGHT))
            for y in range(UNIT, Settings.SCREEN_HEIGHT, UNIT):
                pygame.draw.line(screen, Settings.LINE_COLOR, (0, y), (Settings.SCREEN_WIDTH, y))
        
        bullets.draw(screen)
        targets.draw(screen)
        shooters.draw(screen)
        
        pygame.display.flip()
        clock.tick(Settings.FPS)


if __name__ == "__main__":
    main()