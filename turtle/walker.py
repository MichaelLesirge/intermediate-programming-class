import random
import turtle

from shape_drawer import ShapeDrawer

import pandas as pd
from matplotlib import pyplot as plt

class Walker():
    def __init__(self, shape_sides: int, distance: float, start: turtle.Vec2D = (0, 0)) -> None:
        
        self.tur = turtle.Turtle()
        
        self.tur.pu()
        self.tur.goto(start)
        self.tur.pd()
        
        self.tur.color(random.random(), random.random(), random.random())
        
        self.shape_sides = shape_sides
        self.degrees = 360 / self.shape_sides  
        self.distance = distance
        
        self.start_pos = self.tur.pos()
        
        self.sides = shape_sides
                            
    def step(self):
        self.tur.left(self.degrees * random.randrange(self.shape_sides))
        self.tur.forward(self.distance)
    
    def get_distance_from_start(self) -> float:
        current_pos = self.tur.pos()
        return ((self.start_pos[0] - current_pos[0]) ** 2 + (self.start_pos[1] - current_pos[1]) ** 2) ** 0.5
        
    def shape_step(self):
        for i in range(self.sides):
            self.tur.forward(self.distance)
            self.tur.left(self.degrees)
        
        self.tur.left(random.randint(0, self.sides) * self.degrees)
        self.tur.forward(self.distance)
     
def main():
    turtle.tracer(False)
    
    distance = 7
    num_of_walkers = 30
    num_of_steps = 100
    
    turtle.tracer(False)
    
    turtle.setworldcoordinates(0, 0, turtle.window_width(), turtle.window_height())
    
    s = ShapeDrawer()
    
    num_of_shapes_in_row = 3
    num_of_shapes_in_col = 3
    start_at = 2
    
    shape_size = 75
    
    walker_groups: dict[int, list[Walker]] = {}
    
    for i in range(num_of_shapes_in_row):
        for j in range(num_of_shapes_in_col):
            
            shape_sides = i + ((num_of_shapes_in_col-j-1) * num_of_shapes_in_col) + start_at
            row = turtle.window_width() / num_of_shapes_in_row
            col = turtle.window_height() / num_of_shapes_in_col
            start_point = (row * i + row / 2, col * j + col / 2)
                        
            s.tp(start_point, heading=0).inscribed_circle(shape_sides, shape_size)
            walker_groups[shape_sides] = [Walker(shape_sides, distance, start_point) for i in range(num_of_walkers)]
        
    turtle.update()
    
    for i in range(num_of_steps):
        for walker_group in walker_groups.values():
            for walker in walker_group:
                walker.step()
        turtle.update()
    
    num_of_bins = num_of_walkers
    
    df = pd.DataFrame({sides: [walker.get_distance_from_start() for walker in walker_group] for sides, walker_group in walker_groups.items()})
    df2 = df[sorted(list(walker_groups.keys()))]
    df2.plot.hist(stacked=True, bins=num_of_bins)
    plt.show()
                 
def graph_distance(num_of_walkers = 100, shape_sides = 4, num_of_steps = 50, distance = 10):    
    # num_of_walkers = int(input("number of walker: "))
    # shape_sides = int(input("number of sides of shape: "))
    # num_of_steps = int(input("number of steps: "))
    # distance = int(input("number of pixels to walk each step"))
    
    turtle.tracer(False)
    
    walkers = [Walker(shape_sides, distance) for i in range(num_of_walkers)]
    
    for i in range(num_of_steps):
        for walker in walkers:
            walker.step()
        turtle.update()
    
    number_of_bins = num_of_walkers // 10
    distances = [walker.get_distance_from_start() for walker in walkers]

    df = pd.DataFrame(distances, columns=["distance"])
    df.plot.hist(bins=number_of_bins, alpha=0.5)
    plt.show()
        

if __name__ == "__main__":
    main()