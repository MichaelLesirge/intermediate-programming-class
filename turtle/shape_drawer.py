import turtle
import math

class ShapeDrawer:
    def __init__(self) -> None:
        self.tur = turtle.Turtle()

    def shift(self, d_pos, d_heading = 0) -> "ShapeDrawer":
        """Moves al turtle by dx and dy"""
        self.tp(self.tur.pos() + d_pos, self.tur.heading() + d_heading)

        return self
    
    def tp(self, pos, heading=None) -> "ShapeDrawer":
        """
        Go to x, y cords with out drawing.
        If reset is True it sets itself to looking to {reset heading} which be default is left
        if wait is True then it sleeps
        """
        self.tur.penup()
        self.tur.goto(pos)
        self.tur.pendown()
        
        if heading is not None:
            self.tur.setheading(heading)
        
        return self
    
    def reset(self):
        return self.tp((0, 0), heading=0)
        
        
    def move(self, sides: int, degrees, distance, heading=None) -> "ShapeDrawer":
        """
        if heading is not None then it sets the heading to that number
        draws a {distance} long line then self.turns {degrees} degrees then repeats {sides} times
        """
        if heading is not None:
            self.tur.setheading(heading)
                
        for i in range(sides):
            self.tur.forward(distance)
            self.tur.left(degrees)
        
        return self
    
    def draw_shape_radius(self, sides: int, height: int, fill=False, heading=None, center_x = False, center_y = False) -> "ShapeDrawer":
        degrees = 360 // sides
                    
        if fill:
            if fill is not True: self.tur.fillcolor(fill)
            self.tur.begin_fill()
        
        distance = (2 * height) * math.tan(math.pi/sides)
        if sides == 3: distance =  (2 * height) * (2 / math.sqrt(sides))
        
        if center_x: self.shift((-distance/2, 0))
        if center_y: self.shift((0, -distance/2))
                   
        self.move(sides, degrees, distance, heading)
        
        if center_x: self.shift((distance/2, 0))
        if center_y: self.shift((0, distance/2))
        
        if fill: self.tur.end_fill()
                
        return self
    
    def inscribed_circle(self, corners: int, radius: int, center_y: bool = True) -> "ShapeDrawer":
        
        start_pos = self.tur.pos()
        
        self.shift((0, radius * (1 if center_y else 2)))
        
        self.tur.circle(-radius, extent=360, steps=corners)
        
        self.tp(start_pos)
        
        return self
        
        
    def draw_shape(self, sides: int, distance: int, fill=False, heading=None) -> "ShapeDrawer":
        """
        just enter the number of sides you want and the rest is auto
        you can also enter scale to change the size. scale is set to 1 by default
        if you want 
        """
        degrees = 360 // sides
        
        if fill: self.tur.begin_fill()
                    
        self.move(sides, degrees, distance, heading)
        
        if fill: self.tur.end_fill()
        
        return self
    
def reset(s: ShapeDrawer, delay_seconds=0):
    turtle.delay(delay_seconds * 1000)
    s.reset()
    s.tur.clear()

def main() -> None:
    s = ShapeDrawer()
    
    radius = 100

    turtle.circle(radius)
            
    for i in range(3, 10):
        s.draw_shape_radius(i, radius, center_x=True).reset()
    
    turtle.mainloop()
    
if __name__ == "__main__":
    main()