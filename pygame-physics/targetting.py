# Math and code for this done by much smarter friend, I only cleaned it up

from typing import Any
import pygame

import math
import random
import time

UNIT = 50

class PhysicsConstants:
    GRAVITY = 9.81 * UNIT

class Settings:
    FPS = 60

    SHOOTER_START = [(6 * UNIT, 13 * UNIT)]
    SCREEN_WIDTH, SCREEN_HEIGHT = 21 * UNIT, 15 * UNIT

    BALL_VELOCITY = 11.5 * UNIT
    
    DRAW_GRID = True

    AUTO_FIRE_MODE = True
        
    AIM_ASSIST_START = True
    HIGH_ARK_MODE = False

    BACKGROUND = (255, 255, 255)

    LINE_COLOR = (100, 100, 100)

    NUM_OF_TARGETS = 0

pygame.init()
CLOCK = pygame.time.Clock()

FONT = pygame.font.Font('freesansbold.ttf', 16)

class Target(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SIZE = 0.2 * UNIT

    def __init__(self, location: tuple[int, int], color = COLOR) -> None:
        super().__init__()
                
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill(color)
        
        self.rect = self.image.get_rect(center = location)
        pygame.draw.rect(self.image, color, self.rect)

    def update(self, bullets: pygame.sprite.Group) -> None:
        hit_by = pygame.sprite.spritecollide(self, bullets, dokill=True)
        if hit_by: self.kill()

def random_position() -> tuple[int, int]:
    return (random.randrange(0, Settings.SCREEN_WIDTH, UNIT) + UNIT / 2, random.randrange(0, Settings.SCREEN_HEIGHT, UNIT) + UNIT / 2)

def on_screen(location: tuple[int, int], off_by: int = 0) -> bool:
    x, y = location
    return (-off_by < x < Settings.SCREEN_WIDTH + off_by) and (-off_by < y < Settings.SCREEN_HEIGHT + off_by)

class Bullet(pygame.sprite.Sprite):
    COLOR_DEFAULT = (0, 0, 0)
    COLOR_SPECIAL = (0, 155, 255)
    RADIUS = 0.1 * UNIT

    KILL_OUTSIDE = UNIT * 20

    def __init__(self, location: tuple[int, int], velocity: float, angle: float, color: pygame.Color = COLOR_DEFAULT) -> None:
        super().__init__()
        self.time = 0
        self.init_x, self.init_y = location
        self.x, self.y = self.init_x, self.init_y
        self.init_v = velocity

        self.angle = angle

        # self.image = pygame.Surface((self.RADIUS*2, self.RADIUS*2))
        self.image = pygame.Surface((self.RADIUS * 2, self.RADIUS * 2), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(center=location)

        color = color or (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pygame.draw.circle(self.image, color, (self.RADIUS, self.RADIUS), self.RADIUS, 1)
    
    def find_position(self, time: float) -> tuple[float, float]:
        x = self.init_x + self.init_v * time * math.cos(self.angle)
        y = self.init_y + self.init_v * time * math.sin(self.angle)+(PhysicsConstants.GRAVITY/2*pow(time, 2))
        return x, y
    
    def update(self) -> None:
        self.time += 1/Settings.FPS
        self.x, self.y = self.find_position(self.time)
        self.rect.center = (int(self.x), int(self.y))
        
        if not on_screen(self.rect.center, self.KILL_OUTSIDE):
            self.kill()

class Tracer(Bullet):    
    def find_end_time(self, target: pygame.Rect) -> float:
        while on_screen(self.rect.center, self.KILL_OUTSIDE):
            self.update()
            if self.rect.colliderect(target): break
        return self.time

class Shooter(pygame.sprite.Sprite):
    COLOR = (0, 0, 0)
    RADIUS = 0.5 * UNIT
    BARREL_WIDTH = (RADIUS, 5)
    
    COOL_DOWN = 0.25
    
    def __init__(self, location: tuple[int, int], color = COLOR) -> None:
        super().__init__()

        self.x, self.y = location
        
        self.next_fire_time = time.time() + self.COOL_DOWN

        radius = self.RADIUS
        circumference = self.RADIUS * 2 
        
        self.image = pygame.Surface((circumference , circumference), pygame.SRCALPHA, 32).convert_alpha()
        
        
        self.angle = 0
        
        # pygame.draw.circle(self.image, Settings.BACKGROUND, (radius, radius), radius)
        pygame.draw.circle(self.image, color, (radius, radius), radius, 3)
        pygame.draw.rect(self.image, color, pygame.Rect((radius, radius - self.BARREL_WIDTH[1] / 2), self.BARREL_WIDTH))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        self.image = pygame.transform.rotate(self.image, self.angle)
        
        self.image_start = self.image
        
    def update(self) -> None:
        angle_degrees = (self.angle * 180 / math.pi) % 360
        self.image = pygame.transform.rotate(self.image_start, -angle_degrees)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        

    def find_angle(self, target: tuple[int, int], aim_assist: bool, velocity: float) -> float:
        target_x, target_y = target
        x = target_x - self.x
        y = target_y - self.y
        
        if x == 0: return [3 * math.pi / 2, math.pi / 2][y > 0]

        if aim_assist:
            a = PhysicsConstants.GRAVITY*x*x*y/velocity/velocity+x*x
            b = PhysicsConstants.GRAVITY * PhysicsConstants.GRAVITY*pow(x/velocity, 4)
            c = x*x+y*y

            if c == 0:
                return -math.pi/2
            
            cos = pow((a + pow(pow(a, 2)-b*c, 1/2) * [1, -1][Settings.HIGH_ARK_MODE])/(2*c), 1/2)
                        
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
        else:
            angle = math.atan(y/x)
            if target_x-self.x < 0:
                angle += math.pi
        
        return angle

    def shoot(self, target: tuple[int, int], aim_assist: bool, velocity: float, manual: bool = False) -> Bullet:
        current_time = time.time()
        if not (manual or current_time > self.next_fire_time): return
        self.next_fire_time = current_time + self.COOL_DOWN
        angle = self.find_angle(target, aim_assist, velocity)
        
        if angle is None: return
            
        self.angle = angle
            
        return Bullet((self.x, self.y), velocity, angle, color=(Bullet.COLOR_SPECIAL if manual else Bullet.COLOR_DEFAULT))

        
def describe_fire_path(screen: pygame.Surface, shooter: Shooter, aim_assist: bool = True, ark_line: bool = True):
    color = (52, 161, 235)
    max_box_size = 10
    
    mouse = pygame.mouse.get_pos()
    
    x, y = shooter.rect.center
    tx, ty = mouse
    
    angle = shooter.find_angle(mouse, aim_assist, Settings.BALL_VELOCITY)
    
    target = Target(mouse, color=("green" if angle else "red"))
    
    if angle:
        shooter.angle = angle
        
        angle_degrees = (angle % (2*math.pi)) * (180/math.pi)

        angle_degrees_from_ground = (angle_degrees + 90) % 360
        if angle_degrees_from_ground > 180: angle_degrees_from_ground = 360 - angle_degrees_from_ground
        angle_degrees_from_ground = -(angle_degrees_from_ground - 90)
        
        fire_angle_text = FONT.render(f"Fire at {angle_degrees_from_ground:.0f}°", True, "black")
        
        if ark_line and aim_assist:  
            tracer = Tracer((x, y), Settings.BALL_VELOCITY, angle)
            time = tracer.find_end_time(target)
            
            time_jump = time / 10
                        
            position = tracer.find_position(time)
            
            while time > 0:
                pygame.draw.circle(screen, color, position, 4)
                time -= time_jump
                position = tracer.find_position(time)
                
            pygame.draw.circle(screen, color, tracer.find_position(0), 4)                 
    else:
        fire_angle_text = FONT.render(f"Out of range", True, "black")
            
                
    if ark_line and not aim_assist: pygame.draw.line(screen, color, (x, y), (tx, ty), 2)
    
    pygame.draw.line(screen, color, (x, y), (tx, y), 3)
    horizontal_line_text = FONT.render(f"{abs(tx - x) / UNIT:.1f}", True, "black")
    screen.blit(horizontal_line_text, ((x + tx) / 2, y - [0, horizontal_line_text.get_height()][ty > y]))
    
    pygame.draw.line(screen, color, (tx, y), (tx, ty), 3)
    vertical_line_text = FONT.render(f"{abs(ty - y) / UNIT:.1f}", True, "black")
    screen.blit(vertical_line_text, (tx - [0, horizontal_line_text.get_width()][tx < x], (y + ty) / 2))
    
    min_distance = min(abs(tx - x), abs(ty-y))
    
    if min_distance != 0:
        box_size = min(max_box_size, min_distance)
        pygame.draw.rect(screen, color, pygame.Rect(tx + [0, -box_size][tx > x], y - [box_size, 0][ty > y], box_size, box_size), 2)
    
    screen.blit(target.image, target.rect)
    
    screen.blit(fire_angle_text, (shooter.x - fire_angle_text.get_rect().width/2, shooter.y + shooter.RADIUS))
            

def main() -> None:
    width, height = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT
 
    screen = pygame.display.set_mode((width, height))

    shooters = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    
    # shooters.add(Shooter((width // 2, height // 2)))
    # shooters.add(Shooter(random_position()))
    for position in Settings.SHOOTER_START:
        shooters.add(Shooter(position))

    targets = pygame.sprite.Group()
    
    tracer_shooter = 0
     
    going = True
        
    aim_assist = Settings.AIM_ASSIST_START
    aim_assist_line = True
    
    info_on = 1000
    
    info = FONT.render("Left click to shoot, M to cycle firing display, A to toggle smart aim.", True, (0, 0, 0))

    print("Controls")
    print("Left Click: Fire at mouse")
    print("Right Click: Place shooter")
    
    print("Cycle firing view: M")
    print("Toggle firing view line: K")
    print("Toggle smart aim: A")
    
    print("Place target: T")
    print("Place random target: F")
    

    while going:     
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for shooter in shooters:
                        bullet = shooter.shoot(pygame.mouse.get_pos(), aim_assist, Settings.BALL_VELOCITY, manual = True)
                        if bullet: bullets.add(bullet)
                elif event.button == 3:
                    shooters.add(Shooter(pygame.mouse.get_pos()))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    targets.add(Target(random_position()))
                elif event.key == pygame.K_t:
                    targets.add(Target(pygame.mouse.get_pos())) 
                elif event.key == pygame.K_m:
                    aim_assist_line = True
                    tracer_shooter = (tracer_shooter + 1) % (len(shooters) + 1)
                elif event.key == pygame.K_a:
                    aim_assist = not aim_assist
                elif event.key == pygame.K_l:
                    aim_assist_line = not aim_assist_line

        if Settings.AUTO_FIRE_MODE and targets:
            for shooter in shooters:
                target: Target = random.choice(targets.sprites())
                bullet = shooter.shoot(target.rect.center, aim_assist, Settings.BALL_VELOCITY, manual = False)
                if bullet: bullets.add(bullet)
                    
        if len(targets) < Settings.NUM_OF_TARGETS:
            new_target = Target(random_position())
            targets.add(new_target)

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
        
        if tracer_shooter != 0:
            describe_fire_path(screen, shooters.sprites()[tracer_shooter - 1], aim_assist, aim_assist_line)
        
        if info_on:
            screen.blit(info, (0, 0))
            info_on -= 1
        
        pygame.display.flip()
        CLOCK.tick(Settings.FPS)


if __name__ == "__main__":
    main()
