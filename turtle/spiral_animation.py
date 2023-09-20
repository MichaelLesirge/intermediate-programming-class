import time
import turtle
import random
from spiral import Spiral


def is_turtle_on_screen(t):
    x, y = t.xcor(), t.ycor()
    screen_width = turtle.window_width() / 2
    screen_height = turtle.window_height() / 2

    return -screen_width < x < screen_width and -screen_height < y < screen_height


def main():
    turtle.bgcolor("black")
    turtle.tracer(False)
    turtle.hideturtle()
    
    spirals: list[Spiral] = []

    number_of_spirals = 3

    while True:
        if (random.randint(0, 200) == 0 and len(spirals) < number_of_spirals) or random.randint(0, 1000) == 0:
            spiral = Spiral(
                location=(random.randint(-300, 300),
                          random.randint(-300, 300)),
                scale=random.randint(2, 5) / 10,
                num_of_segments=min(random.randint(2, 10), 4),
                segment_gap=random.randint(7, 13),
                number_of_arms=max(random.randint(-5, 5), 1),
            )
            spirals.append(spiral)

        for spiral in spirals:
            spiral.spin()
            spiral.move()
            spiral.d_location = (min(spiral.d_location[0] + (random.random() - 0.5) / 5, 1), min(
                spiral.d_location[1] + (random.random() - 0.5) / 5, 1))

            if not is_turtle_on_screen(spiral):
                spiral.reset()
                spirals.remove(spiral)

        turtle.update()


if __name__ == "__main__":
    main()
