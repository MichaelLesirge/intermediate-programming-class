import turtle
import colorsys
import time

class Spiral(turtle.Turtle):
    def __init__(self, location: tuple[int, int] = (0, 0), scale = 1.0, start_hue = 0.0, color_change = 1.0, num_of_segments = 4, segment_gap = 10, number_of_arms = 1) -> None:
        super().__init__(visible=False, undobuffersize=0)

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

def main():    
    turtle.bgcolor("black")
    turtle.tracer(False)
    turtle.hideturtle()
    
    spiral_pool = [
        Spiral(scale = 1.0, color_change = 1, num_of_segments = 4, segment_gap = 10, number_of_arms = 3),
        Spiral(scale = 0.7, color_change = 1, num_of_segments = 4, segment_gap = 5, number_of_arms = 1),
        Spiral(scale = 1.3, color_change = 2, num_of_segments = 3, segment_gap = 10, number_of_arms = 1),
        Spiral(scale = 1.0, color_change = 1, num_of_segments = 4, segment_gap = 5, number_of_arms = 3),
        Spiral(scale = 0.6, color_change = 0.5, num_of_segments = 6, segment_gap = 20, number_of_arms = 2),
        Spiral(scale = 0.7, color_change = 1, num_of_segments = 4, segment_gap = 2, number_of_arms = 4),
        Spiral(scale = 1, color_change = 10, num_of_segments = 4, segment_gap = 10, number_of_arms = 1),
        Spiral(scale = 1.1, color_change = 7, num_of_segments = 10, segment_gap = 3, number_of_arms = 1),
        Spiral(scale = 2, color_change = 0.1, num_of_segments = 2, segment_gap = 3, number_of_arms = 1),
    ]
    
    spin_time = 5
    
    while len(spiral_pool) > 0:
        
        end_time = time.time() + spin_time
        
        spiral = spiral_pool.pop(0)
        # spiral = spiral_pool.pop()
        
        while time.time() < end_time:
            spiral.spin()
            turtle.update()
        
        spiral.reset()
             
        
if __name__ == "__main__":
    main()
