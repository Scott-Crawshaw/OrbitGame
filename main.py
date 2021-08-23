import tkinter
import math
from PIL import Image,ImageTk
import time
 
# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

EARTH_X = WINDOW_WIDTH//2
EARTH_Y = WINDOW_HEIGHT//2

EARTH_DIAMETER = WINDOW_HEIGHT//3

SAT_DIAMETER = EARTH_DIAMETER//9

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
        draw_text(angle)
        window.update()

def draw_text(angle):
    global text_id
    canvas.delete(text_id)
    text_id = canvas.create_text(WINDOW_WIDTH-100, 50, text="Angle: %d°" % angle)

def launch(event):
    global launched
    if not launched:
        canvas.delete(line_id)
        launched = True
        x_speed = (event.x - sat_x)/100
        y_speed = (event.y - sat_y)/100
        while True:
            canvas.move(sat_id, x_speed, y_speed)
            window.update()

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

# Add text
text_id = canvas.create_text(WINDOW_WIDTH-100, 50, text="Angle: 0°")

# Binds
window.bind('<Motion>', mouse_moved)
window.bind('<Button>', launch)

window.update()

tkinter.mainloop()