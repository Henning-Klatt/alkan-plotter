from vapory import *
import json
from pprint import pprint
from moviepy.editor import VideoClip

with open('data.json') as data_file:
    data = json.load(data_file)

obj = []

def make_scene(t, x):
    camera = Camera( 'location', [20,20,-40], 'look_at', [0,0,0])
    return Scene( camera, objects= obj, included=["glass.inc"])

def make_frame(t):
    #return scene.render("test.png", width=1024, height=512, antialiasing = 0.01, quality=100)
    return make_scene(t, 1).render(width=1024, height=512, antialiasing = 0.01, quality=100)

def render(data, length, shrink, x, y, z):
    if isinstance(data, list):
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1])))) # Create C node
        createC(x,y,z)
        for i,item in enumerate(data): # Create New nodes around C
            if len(data) == 3:
                if i == 2:
                    x_new = x + length; y_new = y
                    len_new = length
                elif i == 1:
                    x_new = x; y_new = y + length
                    len_new = length - shrink
                elif i == 0:
                    x_new = x; y_new = y - length
                    len_new = length - shrink
            if len(data) == 4:
                if i == 3:
                    x_new = x + length; y_new = y
                    len_new = length
                elif i == 2:
                    x_new = x - length; y_new = y
                    len_new = -length
                elif i == 1:
                    x_new = x; y_new = y + length
                    len_new = length - shrink
                elif i == 0:
                    x_new = x; y_new = y - length
                    len_new = length - shrink
            obj.append(Cylinder([x,y,z], render(item, len_new, shrink, x_new, y_new, z), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
    elif data == 'h': # Create new h node
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.9,0.9,0.9]))))#White color
        createh(x,y,z)
    return [x,y,z]

def createC(x,y,z):
    print("c: " + str(x) + " " + str(y) + " " + str(z))

def createh(x,y,z):
    print("h: " + str(x) + " " + str(y) + " " + str(z))

render(data, 10, 7,  0, 0, 0)

obj.append(LightSource( [10, 120, -40], 'color', [1.3, 1.3, 1.3]))
obj.append(Background("color", [1,1,1]))

wall = Plane([0, 0, 1], 20, Texture(Pigment('color', [1, 1, 1])))
ground = Plane( [0, 1, 0], 0,
                Texture( Pigment( 'color', [1, 1, 1]),
                         Finish( 'phong', 0.1,
                                 'reflection',0.4,
                                 'metallic', 0.3)))

VideoClip(make_frame, duration=1).write_gif("anim.gif",fps=1)
