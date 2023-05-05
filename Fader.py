from turtle import Screen, Turtle
import math

PEN_WIDTH = 5
SEGMENTS_PER_LINE = 12
MILLISECONDS_PER_FADE = 100
AMOUNT_PER_FADE = 0.02

def fade_forward(t, old_location, new_location):
    distance = math.sqrt((new_location[0] - old_location[0])**2 + (new_location[1] - old_location[1]))
    stride = delta = distance / SEGMENTS_PER_LINE
    heading = t.heading()

    while stride < distance:
        position = t.position()
        t.goto(new_location)

        fader = faders.pop() if faders else fader_prototype.clone()
        fader.setheading(heading)
        fade(fader, position, delta)

        t.clear()
        stride += delta

def goto_fade(f, old_location, new_location, shade=0.0):
    distance = math.sqrt((new_location[0] - old_location[0])**2 + (new_location[1] - old_location[1]))
    screen.tracer(False)
    f.clear()

    if shade < 1.0:
        f.pencolor(shade, shade, shade)
        #f.setposition(old_location)
        #f.pendown()
        f.goto(new_location)
        #f.penup()

        shade += AMOUNT_PER_FADE
        screen.ontimer(lambda: goto_fade(f, old_location, new_location, shade), MILLISECONDS_PER_FADE)
    else:
        faders.append(f)

    screen.tracer(True)


def fade(f, position, distance, shade=0.0):
    screen.tracer(False)
    f.clear()

    if shade < 1.0:
        f.pencolor(shade, shade, shade)
        f.setposition(position)
        f.pendown()
        f.forward(distance)
        f.penup()

        shade += AMOUNT_PER_FADE
        screen.ontimer(lambda: fade(f, position, distance, shade), MILLISECONDS_PER_FADE)
    else:
        faders.append(f)

    screen.tracer(True)

faders = []

screen = Screen()

fader_prototype = Turtle()
fader_prototype.hideturtle()
fader_prototype.speed('fastest')
fader_prototype.width(PEN_WIDTH)
fader_prototype.penup()
