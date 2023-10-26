# Math and code for this done by much smarter friend, I only cleaned it up

import pygame
import sys
import math
import random
import enum

class Colors:
    LINE_COLOR = (100, 100, 100)
    BACKGROUND = (255, 255, 255)
    
    DEFAULT_BULLET_COLOR = (0, 0, 0)
    PLAYER_BULLET_COLOR = (0, 100, 255)

class AimTypes(enum.Enum):
    AIMED = enum.auto()
    MANUAL = enum.auto()

def new_target(init_x="r", init_y="r"):
    global targets, shooters, should_auto_shoot
    if len(shooters) > 0:
        if init_x == "r":
            x, y = 525+50*random.randint(-10, 10), 375+50*random.randint(-4, 6)
        else:
            x, y = init_x, init_y
        target = Target(x, y)
        targets.append(target)

        new = random.choice(shooters).new_bullet(x, y, target=target, color=Colors.DEFAULT_BULLET_COLOR)

        if new:
            if should_auto_shoot:
                bullets.append(new)
        else:
            for shooter in shooters:
                new = shooter.new_bullet(x, y, target=target, color=Colors.DEFAULT_BULLET_COLOR)
                if new:
                    if should_auto_shoot:
                        bullets.append(new)
                    break
            if not new:
                targets.remove(target)
                if init_x == "r":
                    new_target()


class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rect(self):
        return pygame.Rect(self.x-meter/6, self.y-meter/6, meter/3, meter/3)

    def display_rect(self, camx, camy, scale=1):
        return pygame.Rect((self.x-meter/6-camx)*scale, (self.y-meter/6-camy)*scale, scale*meter/3, scale*meter/3)

    def draw(self, w, camx, camy, scale=1):
        pygame.draw.rect(w, (255, 0, 0), self.display_rect(
            camx, camy, scale=scale), 2)


class Bullet:
    def __init__(self, x, y, v, angle, target=False, color = (0, 0, 0)):
        self.t = 0
        self.x, self.y = x, y
        self.init_x, self.init_y = x, y
        self.init_v = v
        
        self.angle = angle
        self.target = target
        self.color = color

    def move(self, bullets, targets):
        self.t += 1/fps
        self.x = self.init_x+self.init_v*self.t*math.cos(self.angle)
        self.y = self.init_y+self.init_v*self.t * \
            math.sin(self.angle)+(g/2*pow(self.t, 2))
        rect = pygame.Rect(self.x-meter/10, self.y-meter/10, meter/5, meter/5)
        if self.target:
            if rect.colliderect(self.target.rect()):
                i = 0
                while i < len(targets):
                    if rect.colliderect(targets[i].rect()):
                        targets.remove(targets[i])
                        new_target()
                        if self in bullets:
                            bullets.remove(self)
                    else:
                        i += 1
                self.target = False
        else:
            for target in targets:
                if rect.colliderect(target.rect()):
                    targets.remove(target)
                    bullets.remove(self)
                    new_target()
                    break

    def draw(self, w, camera_x, camera_y, scale=1):
        pygame.draw.circle(w, self.color, (scale*(self.x-camera_x),
                           scale*(self.y-camera_y)), scale*meter/10, 2)


class Shooter:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def new_bullet(self, tx, ty, aim_type: AimTypes = AimTypes.AIMED, v=400, target=False, color=(0, 0, 0)):
        x = tx-self.x
        y = ty-self.y

        match aim_type:
            case AimTypes.MANUAL:
                angle = math.atan(y/x)
                if tx-self.x < 0:
                    angle += math.pi
            case AimTypes.AIMED:
                a = g*x*x*y/v/v+x*x
                b = g*g*pow(x/v, 4)
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
                                if y < v*v/2/g:
                                    print("Impossible location")
                                    return
                                angle *= -1
                        elif cos*(y-g*x*x/2/v/v/cos/cos)/x < 0:
                            angle *= -1
                    except:
                        print("Impossible location")
                        return

        return Bullet(self.x, self.y, v, angle, target=target, color=color)

    def draw(self, w, camx, camy, scale=1):
        pygame.draw.circle(w, (0, 0, 0), (scale*(self.x-camx),
                           scale*(self.y-camy)), scale*meter/2, 2)


def draw_all(screen, camera_x, camera_y, shooters, bullets, targets, grid=True):
    screen.fill(Colors.BACKGROUND)
    width = screen.get_width()
    height = screen.get_height()
    if grid:
        for i in range(math.ceil(height/(meter*scale))):
            pygame.draw.line(screen, Colors.LINE_COLOR, (0, scale*(-camera_y %
                             meter+(i)*meter)), (width, scale*(-camera_y % meter+(i)*meter)))
        for i in range(math.ceil(width/(meter*scale))):
            pygame.draw.line(screen, Colors.LINE_COLOR, (scale*((i+1)*meter-(camera_x %
                             meter)), 0), (scale*((i+1)*meter-(camera_x % meter)), height))

    for target in targets:
        target.draw(screen, camera_x, camera_y, scale=scale)
    for bullet in bullets:
        bullet.draw(screen, camera_x, camera_y, scale=scale)
    for shooter in shooters:
        shooter.draw(screen, camera_x, camera_y, scale=scale)
 
# controls
up, down, left, right, zoom_out, zoom_in = False, False, False, False, False, False

# constants
meter = 50
scale = 1
g = 9.81*meter
fps = 1000

w = pygame.display.set_mode([1000, 750])
clock = pygame.time.Clock()

aim_type = AimTypes.AIMED

should_auto_shoot = False

number_of_targets = 10

sx, sy = 0, 0
x, y = 0, 0
speed_x, speed_y = 0, 0
camera_x, camera_y = 25, 25

shooters = [Shooter(525, 375)]
bullets = []
targets = []
for i in range(number_of_targets):
    new_target()
    pass

while True:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                sys.exit()
            case pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                shooters.append(Shooter(x/scale+camera_x, y/scale+camera_y))
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_SPACE:
                        x, y = pygame.mouse.get_pos()
                        for shooter in shooters:
                            new = shooter.new_bullet(
                                x/scale+camera_x, y/scale+camera_y, color=Colors.PLAYER_BULLET_COLOR, aim_type=aim_type)
                            if new:
                                bullets.append(new)
                    case pygame.K_w:
                        up = True
                    case pygame.K_s:
                        down = True
                    case pygame.K_a:
                        left = True
                    case pygame.K_d:
                        right = True
                    case pygame.K_UP:
                        zoom_in = True
                    case pygame.K_DOWN:
                        zoom_out = True
            case pygame.KEYUP:
                match event.key:
                    case pygame.K_w:
                        up = False
                    case pygame.K_s:
                        down = False
                    case pygame.K_a:
                        left = False
                    case pygame.K_d:
                        right = False
                    case pygame.K_UP:
                        zoom_in = False
                    case pygame.K_DOWN:
                        zoom_out = False

    speed_x = (speed_x*pow(0.6, 30/fps))
    speed_y = (speed_y*pow(0.6, 30/fps))

    if up:
        speed_y -= 80/fps
    if down:
        speed_y += 80/fps
    if left:
        speed_x -= 80/fps
    if right:
        speed_x += 80/fps

    if zoom_in or zoom_out:
        cx = camera_x+w.get_width()/2/scale
        cy = camera_y+w.get_height()/2/scale
        if zoom_in: scale *= pow(1.25, 5/fps)
        if zoom_out: scale *= pow(0.8, 5/fps)
        camera_x = cx-w.get_width()/2/scale
        camera_y = cy-w.get_height()/2/scale

    camera_y += speed_y
    camera_x += speed_x

    for bullet in bullets:
        bullet.move(bullets, targets)

    draw_all(w, camera_x, camera_y, shooters, bullets, targets, (x, y))
    pygame.display.flip()
    clock.tick(fps)

def main() -> None:
    pass

if __name__ == "__main__":
    main()