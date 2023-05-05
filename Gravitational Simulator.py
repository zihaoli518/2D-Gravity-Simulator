import math, random, time, turtle
from tkinter import *
import matplotlib 
from PIL import Image,ImageTk

#parameters 
NBodies = 50
G = 1 
SpaceRadius = 1100
MinMass = 100
MaxMass = 500
MaxVelocity = 200 
BodyColor = (180,160,180)
TraceColor = 'cadetblue2'
BackgroundColor = 'white'
Collision_Factor = 5
Slow_Factor = 2

Screen_Width = 4000
Screen_Height = 2500

#initialize lists 
Turtles = []
Masses = []
Xs = []
Ys = []
Vxs = []  
Vys = []
Body_Colors = []

Off_Screen = []

WinX2 = 0
WinY2 = 0

turtle.colormode(255)

#create a new turtle
def newTurtle():
    t=turtle.Turtle()
    Turtles.append(t)
    t.speed(0)
    t.pensize(4)
    return t

#print initial conditions of a turtle
def printBodyInfo(n):
    print('Body', n, 'mass =', Masses[n], ', x =', Xs[n], ', y =', Ys[n], ', vx =', Vxs[n], ', vy =', Vys[n])

#specify turtle's attributes and draw on canvas according to parameters 
def initialize_body(t):
    m=random.randint(MinMass, MaxMass)
    Masses.append(m)
    t.turtlesize(stretch_wid = 0.1 * math.log2(m), stretch_len = 0.1 * math.log2(m))
    t.shape("circle")
    x=random.randint(-SpaceRadius, SpaceRadius)
    Xs.append(x)
    y=random.randint(-SpaceRadius * 0.7, SpaceRadius * 0.7)
    Ys.append(y)
    Vx=random.randint(-MaxVelocity, MaxVelocity)/100
    Vxs.append(Vx)
    Vy=random.randint(-MaxVelocity, MaxVelocity)/100
    Vys.append(Vy)
    Off_Screen.append(False)
    Body_Colors.append(BodyColor)
    t.penup()
    t.goto(x,y)
    t.pendown()

#initialize all turtles   
def setup():
    turtle.tracer(0,0)
    for n in range(NBodies):
        x = newTurtle()
        initialize_body(x)
        printBodyInfo(n)
    turtle.update()

#moves turtle to new location based on old location & velocity
def move_body(n):
    xNew = Xs[n]+Vxs[n]
    yNew = Ys[n]+Vys[n]
    Xs[n] = xNew
    Ys[n] = yNew

    t=Turtles[n]
    t.shape('circle')
    t.turtlesize(stretch_wid = 0.003 * (math.log(Masses[n]))**3, stretch_len = 0.003 * (math.log(Masses[n]))**3)
    t.shape('circle')
    t.hideturtle()
    t.penup()
    if tracer_switch == True:
        t.pensize(0.005*math.log(Masses[n])**3)
        t.pendown()
        t.color(TraceColor)
    t.goto(xNew,yNew)
    t.pendown()
    t.color(Body_Colors[n])
    t.showturtle()

    if xNew < -WinX2 or xNew > WinX2 or yNew < -WinY2 or yNew > WinY2:
        Off_Screen[n] = True

#move all turtles
def move_bodies():
    for n in range(len(Turtles)):
        t=Turtles[n]
        if t != None:
            move_body(n)

#calculate forces between 2 objects according to Newton's law of gravitation, also determine if two objects should combine
def calculate_force(n1,n2):
    m1 = Masses[n1]
    m2 = Masses[n2]
    x1 = Xs[n1]
    x2 = Xs[n2]
    y1 = Ys[n1]
    y2 = Ys[n2]
    dx = x1-x2
    dy = y1-y2
    r = math.sqrt(dx**2+dy**2)
    f = G*(m1*m2)/(r**2)
    angle = math.atan2(dy,dx)

    min_allowed = 0.025 * (math.log(Masses[n1]))**3 + 0.025 * (math.log(Masses[n2]))**3

    if r <= min_allowed:
        combine = True
        #conservation of momentum 
        px = m1 * Vxs[n1]
        py = m1 * Vys[n1]

        fx = -px/m2 
        fy = -py/m2
    else: 
        combine = False
        fx = (f*math.cos(angle))/Slow_Factor
        fy = (f*math.sin(angle))/Slow_Factor
    return fx, fy, combine

#calculate and update the velocity of an object by running its mass and position against every other object 
def accelerate_body(n):
    global Turtles, Masses, Xs, Ys, Vys, Vxs, Body_Colors, Off_Screen

    Copy_of_Turtles = Turtles.copy()
    Copy_of_Masses = Masses.copy()
    Copy_of_Xs = Xs.copy()
    Copy_of_Ys = Ys.copy()
    Copy_of_Vxs = Vxs.copy()
    Copy_of_Vys = Vys.copy()
    Copy_of_Body_Colors = Body_Colors.copy()
    Copy_of_Off_Screen = Off_Screen.copy()

    for x in range(len(Turtles)): 
        if n > len(Copy_of_Turtles): 
            print('n exceeding len(Copy_of_Turtles)')
            break 
        if x != n:
            #print('accelerate_body_start ', 'len(Turtles) = ', len(Turtles), 'body number ', n, 'x: ', x)
            c,d,combine = calculate_force(n,x)
            xa = -c/Copy_of_Masses[n]
            ya = -d/Copy_of_Masses[n]
            VxNew = Copy_of_Vxs[n]+xa
            VyNew = Copy_of_Vys[n]+ya
            Copy_of_Vxs[n] = VxNew
            Copy_of_Vys[n] = VyNew 

            #combine if radiuses of 2 bodies overlap
            if combine == True: 
                print('combine_body_start ', len(Turtles), 'body number ', n, 'x:', x)
                if Copy_of_Masses[n] > Copy_of_Masses[x]:
                    Copy_of_Vxs[n] = (Copy_of_Vxs[n]*Copy_of_Masses[n] + Copy_of_Vxs[x]*Copy_of_Masses[x])/ (Copy_of_Masses[n] * Collision_Factor)
                    Copy_of_Vys[n] = (Copy_of_Vys[n]*Copy_of_Masses[n] + Copy_of_Vys[x]*Copy_of_Masses[x])/ (Copy_of_Masses[n] * Collision_Factor)

                t = Turtles[x]
                t.hideturtle()

                if Copy_of_Masses[x] > Copy_of_Masses[n]:
                    Copy_of_Vxs[n] = (Copy_of_Vxs[n]*Copy_of_Masses[n] + Copy_of_Vxs[x]*Copy_of_Masses[x])/ (Copy_of_Masses[x] * Collision_Factor)
                    Copy_of_Vys[n] = (Copy_of_Vys[n]*Copy_of_Masses[n] + Copy_of_Vys[x]*Copy_of_Masses[x])/ (Copy_of_Masses[x] * Collision_Factor)
                    Copy_of_Ys[n] = Copy_of_Ys[x]
                    Copy_of_Xs[n] = Copy_of_Xs[x]

                Copy_of_Masses[n]=(Copy_of_Masses[n] + Copy_of_Masses[x])
                Copy_of_Turtles.pop(x)
                Copy_of_Masses.pop(x)
                Copy_of_Xs.pop(x)
                Copy_of_Ys.pop(x)
                Copy_of_Vxs.pop(x)
                Copy_of_Vys.pop(x)
                Copy_of_Body_Colors.pop(x)
                Copy_of_Off_Screen.pop(x)
                print('POPPED ', 'len(Turtles) = ', len(Turtles), 'len(Copy_of_Turtles)', len(Copy_of_Turtles))
                
    #print('Updating Turtles...')
    Turtles = Copy_of_Turtles.copy()
    Masses = Copy_of_Masses.copy()
    Xs = Copy_of_Xs.copy()
    Ys = Copy_of_Ys.copy()
    Vxs = Copy_of_Vxs.copy()
    Vys = Copy_of_Vys.copy()
    Body_Colors = Copy_of_Body_Colors.copy()
    Off_Screen = Copy_of_Off_Screen.copy() 
    #print('accelerate_body_ends. ','len(Turtles) = ', len(Turtles), 'len(Copy_of_Turtles)', len(Copy_of_Turtles))

#applies accelerate_body() to all turtles
def accelerate_bodies():
    for n in range(len(Turtles)):
        if n >= len(Turtles): 
            print('n exceeding len(Turtles)')
            break
        else:
            t=Turtles[n]
            if t != None:
                accelerate_body(n)

#update color of turtle based on its new mass 
def update_color(n, amount=20):
    color = Body_Colors[n][0]
    mass = Masses[n]

    if color > (1 + amount):
        updated_color = int((30-math.log(mass**3))*10 + 30)
        updated_color_tuple = (updated_color-amount, updated_color, updated_color+amount)
        Body_Colors[n] = updated_color_tuple

#update color for all turtles
def update_colors():
    for n in range(len(Turtles)):
        if n >= len(Turtles): 
            print('n exceeding len(Turtles)')
            break
        else:
            t=Turtles[n]
            if t != None:
                update_color(n, amount=30)

#determine the most massive object 
def def_max_mass():
    global max_mass, max_mass_index, center_turtle
    max_mass = max(Masses) 
    max_mass_index = Masses.index(max_mass)
    center_turtle = Turtles[max_mass_index]

#recenter screen around the most massive object
def re_center_function():
    def_max_mass()
    x = Xs[max_mass_index]
    y = Ys[max_mass_index]
    llx = x - Screen_Width/4
    lly = y - Screen_Height/4
    urx = x + Screen_Width/4
    ury = y + Screen_Height/4
    turtle.setworldcoordinates(llx=llx, lly=lly , urx=urx, ury=ury)
    cover_turtle = turtle.Turtle()
    canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
    canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=2))

    #erasing the default dot in the center of the screen
    cover_turtle.speed(0)
    cover_turtle.pensize(4)
    cover_turtle.shape('circle')
    cover_turtle.color(BackgroundColor)

def re_center_switch():
    global re_center
    re_center = not re_center
    #re_center = True

def tracer_function():
    global tracer_switch
    tracer_switch = not tracer_switch

def start_switch():
    global start
    start = True

def down_arrow_function():
    global G
    G = G-0.5

def up_arrow_function():
    global G 
    G = G+0.5

def set_up_GUI():
    global root, re_center_button, G_label,NBodies_entry, loop_timer_label, object_counter_label, biggest_mass_label
    root = screen._root

    tracer_button = Button(root, text='Tracer On/Off', command=tracer_function)
    tracer_button.pack(
    ipadx=10,ipady=10,
    expand=True,side='left')

    re_center_button = Button(root, text='Re-Center', command=re_center_switch)
    re_center_button.pack(
    ipadx=10,ipady=10,
    expand=True,side='left')

    down_image_resize = (Image.open('down_arrow.gif')).resize((20,20), Image.ANTIALIAS)
    down_image = ImageTk.PhotoImage(down_image_resize)
    down_button = Button(root, image=down_image, command=down_arrow_function)
    down_button.image = down_image
    down_button.pack(
    ipadx=5,ipady=5,
    expand=False,side='left')

    G_label = Label(root, text='G: ' + str(G))
    G_label.pack(
    ipadx=10,ipady=10,
    expand=False,side='left')

    up_image_resize = (Image.open('up_arrow.gif')).resize((20,20), Image.ANTIALIAS)
    up_image = ImageTk.PhotoImage(up_image_resize)
    up_button = Button(root, image=up_image, command=up_arrow_function)
    up_button.image = up_image
    up_button.pack(
    ipadx=5,ipady=5,
    expand=False,side='left')

    NBodies_label = Label(root, text='Number of Starting Bodies: ')
    NBodies_label.pack(
    ipadx=70,ipady=10,
    expand=False,side='left')

    NBodies_entry = Entry(root, width=5)
    NBodies_entry.insert(0, '70')
    NBodies_entry.pack(
    ipadx=0,ipady=10,
    expand=False,side='left')

    start_button = Button(root, text='START', command=start_switch, height=2, width=10, font='Times 20 bold', borderwidth=20)
    start_button.pack(
    ipadx=20,ipady=5,
    expand=True,side='left')

    loop_timer_label = Label(root, text='Simulation Timer: ' + str(loop_timer))
    loop_timer_label.pack(
    ipadx=10,ipady=10,
    expand=True,side='left')

    object_counter_label = Label(root, text = 'Number of Objects Remaining: ' + str(len(Turtles)))
    object_counter_label.pack(
    ipadx=10,ipady=10,
    expand=True,side='left')

    biggest_mass_label = Label(root, text = 'Largest Mass: ' )
    biggest_mass_label.pack(
    ipadx=10,ipady=10,
    expand=True,side='left')

#putting everything together 
def main():
    print ('N-Body simulation starting')
    global screen, canvas, start
    screen = turtle.Screen()
    canvas = screen.getcanvas()
    canvas.pack(fill="both", expand=True)
    canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
    canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=2))
    screen.bgcolor(BackgroundColor)

    screen.setup(Screen_Height, Screen_Width)
    global WinX2, WinY2
    WinX2 = screen.window_width() / 2
    WinY2 = screen.window_height() / 2

    #set up values for GUI
    screen.title('N-Body Simulator')
    global re_center, loop_timer, tracer_switch
    start = False
    loop_timer = 1
    re_center = False 
    tracer_switch = False
    set_up_GUI()

    #take user inputs 
    while start == False: 
        print('waiting for inputs')
        turtle.update()
        G_label.config(text = 'G: ' + str(G))
        global NBodies
        NBodies = int(NBodies_entry.get())
        time.sleep(0.5)
    
    if start == True: 
        setup()

    #running the actual simulation
    while len(Turtles) > 0:
        if start == True: 
            #sync_lists_1() 
            print('while loop1 start ', loop_timer, 'len(Turtles) = ', len(Turtles), 'len(Turtles)', len(Turtles))
            move_bodies()           
            accelerate_bodies()
            update_colors()
            if re_center == True:
                re_center_function()
                re_center_switch()
                tracer_switch = False 
            print('while loop end ', loop_timer, 'len(Turtles) = ', len(Turtles), 'len(Turtles)', len(Turtles))
            #update GUI display values 
            G_label.config(text = 'G: ' + str(G))
            loop_timer = loop_timer+1
            loop_timer_label.config(text = 'Simulation Timer: ' + str(loop_timer))
            object_counter_label.config(text = 'Ner of Objects Remaining: ' + str(len(Turtles)))
            biggest_mass_label.config(text = 'Largest Mass: ' + str(max(Masses)))

            turtle.update()

    print('Program finished')
    screen.mainloop()


if __name__ == '__main__':
    main()

