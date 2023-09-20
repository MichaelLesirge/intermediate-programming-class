import turtle
import math

class ShapeDrawer:
    def __init__(self) -> None:
        self.tur = turtle.Turtle()

    def shift(self, x = 0, y = 0, heading = 0) -> "ShapeDrawer":
        """Moves al turtle by dx and dy"""
        current_x, current_y = self.tur.pos()
        current_heading = self.tur.heading()
        self.tp(current_x+x, current_y+y, current_heading + heading)

        return self
    
    def tp(self, x=0, y=0, heading=None) -> "ShapeDrawer":
        """
        Go to x, y cords with out drawing.
        If reset is True it sets itself to looking to {reset heading} which be default is left
        if wait is True then it sleeps
        """
        self.tur.penup()
        self.tur.goto(x, y)
        self.tur.pendown()
        
        if heading is not None:
            self.tur.setheading(heading)
        
        return self
    
    def reset(self):
        return self.tp(0, 0, 0)
        
        
    def move(self, sides: int, degrees, distance, heading=None, left=False) -> "ShapeDrawer":
        """
        if heading is not None then it sets the heading to that number
        draws a {distance} long line then self.turns {degrees} degrees then repeats {sides} times
        """
        if heading is not None:
            self.tur.setheading(heading)
                
        adjust = -1 if left else 1        
        for i in range(sides):
            self.tur.forward(distance * adjust)
            self.tur.left(degrees * adjust)
            adjust = 1
        
        return self
    
    def draw_shape_radius(self, sides: int, height: int, fill=False, heading=None, left = False) -> "ShapeDrawer":
        degrees = 360 // sides
        
        if fill:
            if fill is not True: self.tur.fillcolor(fill)
            self.tur.begin_fill()
        
        distance = (2 * height) * math.tan(math.pi/sides)
        if sides == 3: distance =  (2 * height) * (2 / math.sqrt(sides))
                   
        self.move(sides, degrees, distance, heading, left)
        
        if fill: self.tur.end_fill()
        
        return self
        
        
    def draw_shape(self, sides: int, distance: int, fill=False, heading=None, left=False) -> "ShapeDrawer":
        """
        just enter the number of sides you want and the rest is auto
        you can also enter scale to change the size. scale is set to 1 by default
        if you want 
        """
        degrees = 360 // sides
        
        if fill: self.tur.begin_fill()
                    
        self.move(sides, degrees, distance, heading, left)
        
        if fill: self.tur.end_fill()
        
        return self