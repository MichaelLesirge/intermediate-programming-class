# Math and code for this done by much smarter friend, I only cleaned it up

import pygame

import math
import random
import time

UNIT = 50


class PhysicsConstants:
    GRAVITY = 9.81 * UNIT

class Settings:
    FPS = 1000

    SCREEN_WIDTH, SCREEN_HEIGHT = 21 * UNIT, 15 * UNIT

    BALL_VELOCITY = 400

    DRAW_GRID = True

    AUTO_FIRE_MODE = True
        
    AIM_ASSIST_START = True

    BACKGROUND = (255, 255, 255)

    LINE_COLOR = (100, 100, 100)

    NUM_OF_TARGETS = 10

class Target(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    SIZE = 0.2 * UNIT

    def __init__(self, location: tuple[int, int]) -> None:
        super().__init__()
                
        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.rect = self.image.get_rect(center = location)
        pygame.draw.rect(self.image, self.COLOR, self.rect)

    def update(self, bullets: pygame.sprite.Group) -> None:
        hit_by = pygame.sprite.spritecollide(self, bullets, dokill=False)
        if hit_by: self.kill()

def random_position() -> tuple[int, int]:
    return (random.randrange(0, Settings.SCREEN_WIDTH, UNIT) + UNIT / 2, random.randrange(0, Settings.SCREEN_HEIGHT, UNIT) + UNIT / 2)

def on_screen(rect: pygame.Rect, off_by: int = 0) -> bool:
    return (-off_by < rect.x < Settings.SCREEN_WIDTH + off_by) and (-off_by < rect.y < Settings.SCREEN_HEIGHT + off_by)

class Bullet(pygame.sprite.Sprite):
    COLOR_DEFAULT = (0, 0, 0)
    COLOR_SPECIAL = (0, 155, 255)
    RADIUS = 0.1 * UNIT

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
        
        if not on_screen(self.rect, 250):
            self.kill()

class Shooter(pygame.sprite.Sprite):
    COLOR = (0, 0, 0)
    RADIUS = 0.5 * UNIT
    
    COOL_DOWN = 0.25
    
    def __init__(self, location: tuple[int, int]) -> None:
        super().__init__()

        self.x, self.y = location
        
        self.next_fire_time = time.time() + self.COOL_DOWN

        self.image = pygame.Surface((self.RADIUS * 2, self.RADIUS * 2), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        pygame.draw.circle(self.image, self.COLOR, (self.RADIUS, self.RADIUS), self.RADIUS, 3)

    def find_angle(self, target: tuple[int, int], aim_assist: bool, velocity: float) -> float:
        target_x, target_y = target
        x = target_x - self.x
        y = target_y - self.y

        if aim_assist:
            a = PhysicsConstants.GRAVITY*x*x*y/velocity/velocity+x*x
            b = PhysicsConstants.GRAVITY * PhysicsConstants.GRAVITY*pow(x/velocity, 4)
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
        
        return Bullet((self.x, self.y), velocity, angle, color=(Bullet.COLOR_SPECIAL if manual else Bullet.COLOR_DEFAULT))


def main() -> None:
    width, height = Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    shooters = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    
    # shooters.add(Shooter((width // 2, height // 2)))
    shooters.add(Shooter(random_position()))

    targets = pygame.sprite.Group()
     
    going = True

    while going:     
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for shooter in shooters:
                        bullet = shooter.shoot(pygame.mouse.get_pos(), Settings.AIM_ASSIST_START, Settings.BALL_VELOCITY, manual = True)
                        if bullet: bullets.add(bullet)
                elif event.button == 3:
                    shooters.add(Shooter(pygame.mouse.get_pos()))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    targets.add(Target(random_position()))
                elif event.key == pygame.K_r:
                    targets.add(Target(pygame.mouse.get_pos()))
        
        if pygame.key.get_pressed()[pygame.K_m]:
            x, y = pygame.mouse.get_pos()
            

        if Settings.AUTO_FIRE_MODE and targets:
            for shooter in shooters:
                target: Target = random.choice(targets.sprites())
                bullet = shooter.shoot(target.rect.center, Settings.AIM_ASSIST_START, Settings.BALL_VELOCITY, manual = False)
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
        
        pygame.display.flip()
        clock.tick(Settings.FPS)


if __name__ == "__main__":
    main()
