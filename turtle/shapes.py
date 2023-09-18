from shape_drawer import ShapeDrawer

import turtle

def reset(s: ShapeDrawer, delay_seconds=0):
    turtle.delay(delay_seconds * 1000)
    s.reset()
    s.tur.clear()

def main() -> None:
    s = ShapeDrawer()
    
    radius = 100
            
    for i in range(3, 10):
        s.draw_shape_radius(i, radius, center=True).reset()
    
    turtle.mainloop()
    
if __name__ == "__main__":
    main()