import turtle
import colorsys
import random
import time

class Spiral(turtle.Turtle):
    def __init__(self, location: tuple[int, int] = (0, 0), scale = 1.0, start_hue = 0.0, color_change = 1.0, num_of_segments = 4, segment_gap = 10, number_of_arms = 1) -> None:
        super().__init__(visible=False)

        self.start_location = location
        self.scale = scale
        self.start_hue = start_hue
        self.color_change = 0.004 * color_change
        self.num_of_segments = num_of_segments
        self.segment_gap = segment_gap
        self.number_of_arms = number_of_arms
        self.d_location = (0, 0)

        self.hideturtle()
        self.pensize(4)
        self.reset()
    
    def tp(self, location):
        self.location = location
        self.penup()
        self.goto(location)
        self.pendown()

    def reset(self) -> None:
        super().reset()
        self.hue = self.start_hue
        self.tp(self.start_location)

    def draw_shape(self) -> None:
        self.forward(50 * self.scale)
        self.right(20)
        self.forward(40 * self.scale)
        self.right(9)

    def spin(self) -> None:
        start_heading = self.heading()
        
        for arm in range(self.number_of_arms):
            self.setheading(start_heading + arm * (360 / self.number_of_arms))
            color = colorsys.hsv_to_rgb(self.hue, 1, 1)
            self.fillcolor(color)
            for segment in range(self.num_of_segments):

                self.begin_fill()
                self.draw_shape()
                self.end_fill()

                self.hue += self.color_change
            
            self.setheading(start_heading + self.segment_gap)
            self.tp(self.location)
                        
    def shift_by(self, d_location: tuple[float, float]):
        self.tp((self.location[0] + d_location[0], self.location[1] + d_location[1]))

    def move(self):
        self.shift_by(self.d_location)

def is_turtle_on_screen(t):
    x, y = t.xcor(), t.ycor()
    screen_width = turtle.window_width() / 2
    screen_height = turtle.window_height() / 2

    return -screen_width < x < screen_width and -screen_height < y < screen_height

def main():    
    turtle.bgcolor("black")
    turtle.tracer(False)
    
    # s = Spiral(location = (0, 0), scale = 1.0, color_change = 0.03, num_of_segments = 4, segment_gap = 20, number_of_arms = 3)
    # while True:
    #     s.spin()
    #     turtle.update()
    #     time.sleep(0.01)
    #     # s.clear()
     
    spirals: list[Spiral] = []
    
    number_of_spirals = 3
    
    while True:
        if (random.randint(0, 200) == 0 and len(spirals) < number_of_spirals) or random.randint(0, 1000) == 0:
            spiral = Spiral(
                location=(random.randint(-300, 300), random.randint(-300, 300)),
                scale=random.randint(2, 5) / 10,
                num_of_segments=min(random.randint(2, 10), 4),
                segment_gap=random.randint(7, 13),
                number_of_arms=max(random.randint(-5,5), 1),
            )
            spirals.append(spiral)
        
        for spiral in spirals:
            spiral.spin()
            spiral.move()
            spiral.d_location = (min(spiral.d_location[0] + (random.random() - 0.5) / 20, 1), min(spiral.d_location[1] + (random.random() - 0.5) / 20, 1))
            
            if not is_turtle_on_screen(spiral):
                spiral.reset()
                spirals.remove(spiral)
            
            
            
        turtle.update()

if __name__ == "__main__":
    main()
