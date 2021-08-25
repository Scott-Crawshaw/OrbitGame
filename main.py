# Scott Crawshaw
# 8/25/21

import tkinter
import math
from PIL import Image,ImageTk
from shapely.geometry import Polygon
 
# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

EARTH_X = WINDOW_WIDTH//2
EARTH_Y = WINDOW_HEIGHT//2

EARTH_DIAMETER = WINDOW_HEIGHT//3

SAT_DIAMETER = EARTH_DIAMETER//9

GRAVITY = 6.674E-11

EARTH_MASS = 5.972E24

# Variables
sat_x = EARTH_X
sat_y = EARTH_Y - EARTH_DIAMETER//2 - SAT_DIAMETER//6
line_id = None
launched = False
 
# Event handlers
def mouse_moved(event):
    draw_line(sat_x, sat_y, event.x, event.y)

# Helper Functions
def draw_line(start_x, start_y, end_x, end_y):
    if not launched:
        global line_id
        angle = 90 - abs(math.ceil(math.degrees(math.atan2(start_x-end_x, start_y-end_y))))
        if line_id is not None:
            canvas.delete(line_id)
        line_id = canvas.create_line(start_x, start_y, end_x, end_y, dash=(4, 2))
        window.update()

def is_game_over():
    earth_new_x = EARTH_X - (EARTH_DIAMETER/3)
    earth_new_y = EARTH_Y - (EARTH_DIAMETER/3)
    earth_new_diameter = EARTH_DIAMETER*.7
    sat_new_x = sat_x - (SAT_DIAMETER/2)
    sat_new_y = sat_y - (SAT_DIAMETER/2)

    earth_poly = Polygon([(earth_new_x, earth_new_y), (earth_new_x+earth_new_diameter,earth_new_y), (earth_new_x+earth_new_diameter,earth_new_y+earth_new_diameter), (earth_new_x,earth_new_y+earth_new_diameter)])
    sat_poly = Polygon([(sat_new_x, sat_new_y), (sat_new_x+SAT_DIAMETER,sat_new_y), (sat_new_x+SAT_DIAMETER,sat_new_y+SAT_DIAMETER), (sat_new_x,sat_new_y+SAT_DIAMETER)])
    
    if earth_poly.intersects(sat_poly):
        return True
    if sat_x+SAT_DIAMETER < 0 or sat_x > WINDOW_WIDTH or sat_y+SAT_DIAMETER < 0 or sat_y > WINDOW_HEIGHT:
        return True
    return False

def launch(event):
    global launched, sat_x, sat_y
    if not launched:
        canvas.delete(line_id)
        launched = True
        x_speed = (event.x - sat_x)/100
        y_speed = (event.y - sat_y)/100
        while True:
            accel_x, accel_y = calc_accel()
            x_speed += accel_x
            y_speed += accel_y
            canvas.move(sat_id, x_speed, y_speed)
            sat_x += x_speed
            sat_y += y_speed
            window.update()
            if is_game_over():
                reset_game()
                break

def calc_accel():
    dx = (sat_x-EARTH_X)
    dy = (sat_y-EARTH_Y)
    distance = math.sqrt(dx**2 + dy**2)*8
    percent_x = dx / distance
    percent_y = dy / distance
    accel = -((GRAVITY*EARTH_MASS)/(distance**2))/1000000000
    ax = accel * percent_x
    ay = accel * percent_y
    return ax, ay

def reset_game():
    global line_id, launched, sat_id, sat_x, sat_y
    sat_x = EARTH_X
    sat_y = EARTH_Y - EARTH_DIAMETER//2 - SAT_DIAMETER//6
    line_id = None
    launched = False
    canvas.delete(sat_id)
    sat_id = canvas.create_image((sat_x, sat_y), image=sat_img)


# Create the window
window = tkinter.Tk()
window.title("Blast Off!")
window.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))

# Create the canvas
canvas = tkinter.Canvas(window)
canvas.configure(bg="black")
canvas.pack(fill="both", expand=True)

# Add earth
earth_img = ImageTk.PhotoImage(Image.open("earth.png").resize((EARTH_DIAMETER,EARTH_DIAMETER)))
canvas.create_image((EARTH_X, EARTH_Y), image=earth_img)

# Add sat
sat_base_img = Image.open("sat.png").resize((SAT_DIAMETER*2,SAT_DIAMETER))
sat_img = ImageTk.PhotoImage(sat_base_img)
sat_id = canvas.create_image((sat_x, sat_y), image=sat_img)

# Binds
window.bind('<Motion>', mouse_moved)
window.bind('<Button>', launch)

window.update()

tkinter.mainloop()