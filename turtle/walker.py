import random
import turtle

# do pip install matplotlib
import matplotlib.pyplot as plt
import numpy as np        

class Walker():
    def __init__(self, shape_sides: int, distance) -> None:
        
        self.tur = turtle.Turtle()
        self.tur.color(random.random(), random.random(), random.random())
        
        self.degrees = 360 / shape_sides  
        self.distance = distance
        
        self.start_pos = self.tur.pos()
        
        self.sides = shape_sides
                            
    def step(self):
        if random.randint(0, 1): self.tur.left(self.degrees)
        else: self.tur.forward(self.distance)
    
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
    
    num_of_walkers = 100
    # num_of_walkers = int(input("number of walker: "))
    shape_sides = 3
    # shape_sides = int(input("number of sides of shape: "))
    num_of_steps = 500
    # num_of_steps = int(input("number of steps: "))
    
    distance = 10
    # distance = int(input("number of pixels to walk each step"))
    
    turtle.tracer(False)
    
    walkers = [Walker(shape_sides, distance) for i in range(num_of_walkers)]
    
    for i in range(num_of_steps):
        for walker in walkers:
            walker.step()
        turtle.update()
    
    number_of_bins = 10
    distances = [walker.get_distance_from_start() for walker in walkers]
            
    plt.hist(distances, bins=number_of_bins)
    # plt.plot(range(len(distances)), sorted(distances))

    plt.show()
    
    turtle.mainloop()
    

if __name__ == "__main__":
    main()