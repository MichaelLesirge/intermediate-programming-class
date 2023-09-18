
import turtle
from shape_drawer import ShapeDrawer 

def draw_checkers(s: ShapeDrawer, size = 100, dimension = 5, move_to_center = False):
    if move_to_center:
        s.shift(-size * (dimension / 2), -size * (dimension / 2))
    
    for i in range(dimension):
        for j in range(dimension):
            s.draw_shape(4, fill=((i+j) % 2 == 0), distance=size).shift(x=size)
        s.shift(-size*dimension, size)

def draw_boxes(s: ShapeDrawer, num_of_boxes = 5):
    for i in range(num_of_boxes):
        s.draw_shape(4, 50, heading=(360 / num_of_boxes) * i)

def draw_snail(s: ShapeDrawer, num_of_circles = 100, scale = 2):
    for i in range(num_of_circles):
        s.tur.circle(i * scale)
        s.tur.left(2.5 * scale)

def draw_diamond_corner(s: ShapeDrawer, num_of_lines = 10, line_gap_distance = 50, pos = None, x_rotation = 1, y_rotation = 1):    
    # https://docs.google.com/presentation/d/1SqEqX8SOIouH3ASkvaDoHu2sWhU26aGYhcuzizdsvVo/edit#slide=id.g27ce32dd55b_0_53
    x, y = pos or s.tur.pos()
    
    for i in range(num_of_lines + 1):
        s.tp(x_rotation * (x + (num_of_lines - i) * line_gap_distance), y_rotation * y)
        s.tur.goto(x_rotation * x, y_rotation * (y + i * line_gap_distance))
        
    s.tp(x, y)
        
def draw_diamond(s: ShapeDrawer, num_of_lines = 10, line_gap_distance = 50, pos = None):
    for x_rotation in [-1, 1]:
        for y_rotation in [-1, 1]:
            draw_diamond_corner(s, num_of_lines, line_gap_distance, pos, x_rotation, y_rotation)

def reset(s: ShapeDrawer, delay_seconds=0):
    # turtle.delay(delay_seconds * 1000)
    s.reset()
    s.tur.clear()

def main():
    turtle.Screen().bgcolor("black")

    s = ShapeDrawer()
    s.tur.color("chartreuse")
    s.tur.speed(0)
    
    wait = 0.5
    
    s.tp(-100, 100).draw_shape(4, distance=50, fill=False)
    reset(s, delay_seconds=wait)
     
    draw_checkers(s, dimension=5, move_to_center = True)
    reset(s, delay_seconds=wait)
    
    draw_boxes(s, num_of_boxes=5)
    reset(s, delay_seconds=wait)
    
    draw_snail(s, num_of_circles=100)
    reset(s, delay_seconds=wait)
    
    draw_diamond(s, num_of_lines=10, line_gap_distance=20)    
    
    turtle.mainloop()

if __name__ == "__main__":
    main()



