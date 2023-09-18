import turtle
import colorsys

class Spiral(turtle.Turtle):
    def __init__(self, location = (0, 0), scale = 1, spin_speed = 1, start_hue = 0, color_change = 0.004) -> None:
        super().__init__(visible=False)
        self.pensize(4)
       
        self.location = location
        self.scale = scale
        self.spin_speed = spin_speed
       
        self.start_hue = start_hue
        self.color_change = color_change
       
        self.reset()
       
    def tp(self, location):
        self.penup()
        self.goto(location)
        self.pendown()
       
    def reset(self) -> None:
        super().reset()
        self.hue = self.start_hue
        self.tp(self.location)
       
    def draw_shape(self) -> None:
        self.forward(50 * self.scale)
        self.right(20 * self.scale)
        self.forward(40 * self.scale)
        self.right(9 * self.scale)
       
    def next(self) -> None:
        for i in range(4):            
            color = colorsys.hsv_to_rgb(self.hue, 1, 1)
            self.fillcolor(color)
            self.hue += self.color_change
           
            self.begin_fill()
            self.draw_shape()
            self.end_fill()
   
        self.right(self.spin_speed)
        self.tp(self.location)

def main():
    turtle.bgcolor("black")
    turtle.tracer(100)
   
    s = Spiral()
   
    for i in range(400):
        s.next()
       
   


if __name__ == "__main__":
    main()
