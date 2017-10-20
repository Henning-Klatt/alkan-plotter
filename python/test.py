from vapory import *
import json
from pprint import pprint
from moviepy.editor import VideoClip

with open('json-easy.json') as data_file:
    data = json.load(data_file)

obj = []

def make_scene(t, x):
    camera = Camera( 'location', [20,20,-40], 'look_at', [0,0,0])
    return Scene( camera, objects= obj, included=["glass.inc"])

def make_frame(t):
    #return scene.render("test.png", width=1024, height=512, antialiasing = 0.01, quality=100)
    return make_scene(t, 1).render(width=1024, height=512, antialiasing = 0.01, quality=100)

def render(data, length, x, y, z):
    if isinstance(data, list):
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1])))) # Create C node
        createC(x,y,z)
        multiply = [-1,1,1,1]
        for i,item in enumerate(data): # Create New nodes around C
            if i == 1 or i == 0:
                new_y = (y + length) * multiply[i]; new_x = x
                new_length = length - 1
            else:
                new_y = y; new_x = (x + length) * multiply[i]
                new_lenght = length
            obj.append(Cylinder([x,y,z], render(item, new_length, new_x, new_y, z), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
    elif data == 'h': # Create new h node
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1]))))
        createh(x,y,z)
    return [x,y,z]

def createC(x,y,z):
    print("c: " + str(x) + " " + str(y) + " " + str(z))

def createh(x,y,z):
    print("h: " + str(x) + " " + str(y) + " " + str(z))

render(data, 10, 0, 0, 0)

obj.append(LightSource( [10, 120, -40], 'color', [1.3, 1.3, 1.3]))
obj.append(Background("color", [1,1,1]))

wall = Plane([0, 0, 1], 20, Texture(Pigment('color', [1, 1, 1])))
ground = Plane( [0, 1, 0], 0,
                Texture( Pigment( 'color', [1, 1, 1]),
                         Finish( 'phong', 0.1,
                                 'reflection',0.4,
                                 'metallic', 0.3)))

VideoClip(make_frame, duration=1).write_gif("anim.gif",fps=1)
