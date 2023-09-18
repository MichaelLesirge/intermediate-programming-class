import turtle
import colorsys


class Spiral(turtle.Turtle):
    def __init__(self, location: tuple[int, int] = (0, 0), scale = 1.0, color_change = 1.0, num_of_segments = 4, segment_gap = 10, number_of_arms = 1) -> None:
        super().__init__(visible=False)

        self.location = location
        self.scale = scale
        self.color_change = 0.004 * color_change
        self.num_of_segments = num_of_segments
        self.segment_gap = segment_gap
        self.number_of_arms = number_of_arms

        self.hideturtle()
        self.pensize(4)
        self.reset()

    def tp(self, location):
        self.penup()
        self.goto(location)
        self.pendown()

    def reset(self) -> None:
        super().reset()
        self.hue = 0
        self.tp(self.location)

    def draw_shape(self) -> None:
        self.forward(50 * self.scale)
        self.right(20)
        self.forward(40 * self.scale)
        self.right(9)

    def next(self) -> None:
        start_heading = self.heading()
        
        for i in range(self.num_of_segments):
            color = colorsys.hsv_to_rgb(self.hue, 1, 1)
            self.fillcolor(color)

            self.begin_fill()
            self.draw_shape()
            self.end_fill()

            self.hue += self.color_change

        self.setheading(start_heading + self.segment_gap + (360 / self.number_of_arms))
        self.tp(self.location)


def main():
    turtle.bgcolor("black")
    turtle.tracer(20)

    spiral1 = Spiral(location=(0, 0), scale=1, color_change=0.5, num_of_segments=4, segment_gap=5, number_of_arms=3)
    spiral2 = Spiral(location=(0, 0), scale=1, color_change=1, num_of_segments=4, segment_gap=10, number_of_arms=1)

    while True:
        spiral1.next()

if __name__ == "__main__":
    main()
