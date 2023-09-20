import colorsys
import random
import turtle

from shape_drawer import ShapeDrawer

GRAVITY = turtle.Vec2D(0, -0.03)

class Drop():
    def __init__(self, pos: turtle.Vec2D, sides = 4, size = 100, color_change = 1, spin_speed = 1) -> None:
        super().__init__()
        
        self.s = ShapeDrawer()
        self.tur = self.s.tur
         
        self.sides = sides
        self.size = size
        
        self.color_change = color_change
        self.spin_speed = spin_speed
        
        self.hue = 0
        self.rotation = 0
        
        self.s.tp(pos)
        self.momentum = turtle.Vec2D(0, 0)
                
    def draw(self):
        # self.s.draw_shape_radius(self.sides, fill=colorsys.hsv_to_rgb(self.hue, 1, 1), height=self.size, heading=self.rotation, center_x=True, center_y=True)
        # self.hue += self.color_change
        # self.rotation += self.spin_speed
        
    def move(self):
        # self.s.tp(self.tur.pos() + GRAVITY + self.momentum)
    
def main():
    turtle.tracer(False)
    turtle.hideturtle()
    
    sprites: list[Drop] = []
    
    going = True
    
    x, y = turtle.window_width() / 2, turtle.window_height() / 2
        
    while going:
        for drop in sprites:
            drop.tur.clear()
        
        if random.randint(0, 5000) == 0:
            drop = Drop(
                pos=turtle.Vec2D(random.randint(-x, x), y),
                sides=random.randint(3, 10),
                size=random.randint(10, 50),
                spin_speed=random.randint(-10, 10)
            )
            sprites.append(drop)
            
        for drop in sprites:
            drop.draw()
        
        for drop in sprites:
            drop.move()
        
        turtle.update()
        


if __name__ == "__main__":
    main()