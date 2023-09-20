import colorsys
import random
import turtle

from shape_drawer import ShapeDrawer

GRAVITY = turtle.Vec2D(0, -9.8)

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
        
        self.momentum = turtle.Vec2D(0, 0)
                
    def draw(self):
        self.s.draw_shape_radius(self.sides, fill=colorsys.hsv_to_rgb(self.hue, 1, 1), height=self.size, heading=self.rotation)
        self.hue += self.color_change
        self.rotation += self.spin_speed
        
    def move(self):
        self.s.tur.setpos(self.tur.pos() + GRAVITY + self.momentum)
        pass
    
def main():
    turtle.tracer(False)
    turtle.hideturtle()
    
    sprites: list[Drop] = []
    
    going = True
    
    x, y = turtle.window_width(), turtle.window_height()
    
    while going:
        if random.randint(0, 1000) == 0:
            drop = Drop(
                pos=turtle.Vec2D(y, random.randint(-x//2, x//2)),
                sides=random.randint(3, 10),
                size=random.randint(10, 50),
                spin_speed=random.randint(-10, 10)
            )
            sprites.append(drop)
            
        for drop in sprites:
            drop.draw()
        
        for drop in sprites:
            drop.move()
        
        turtle.clear()
        turtle.update()
        


if __name__ == "__main__":
    main()