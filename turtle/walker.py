import turtle
import random
        
class Walker():
    def __init__(self, shape_sides: int, distance) -> None:
        
        self.tur = turtle.Turtle()
        self.tur.color(random.random(), random.random(), random.random())
        
        self.degrees = 360 / shape_sides  
        self.distance = distance
        
        self.sides = shape_sides
                            
    def step(self):
        if random.randint(0, 1): self.tur.left(self.degrees)
        else: self.tur.forward(self.distance)
         
def main():
    
    num_of_walkers = 10
    # num_of_walkers = int(input("number of walker: "))
    shape_sides = 3
    # shape_sides = int(input("number of sides of shape: "))
    num_of_steps = 1000
    # num_of_steps = int(input("number of steps: "))
    
    distance = 10
    # distance = int(input("number of pixels to walk each step"))
    
    turtle.tracer(False)
    
    walkers = [Walker(shape_sides, distance) for i in range(num_of_walkers)]
    
    for i in range(num_of_steps):
        for walker in walkers:
            walker.step()
        turtle.update()

    turtle.mainloop()
    

if __name__ == "__main__":
    main()