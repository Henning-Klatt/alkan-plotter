from vapory import *
import json
from pprint import pprint
from moviepy.editor import VideoClip

with open('data.json') as data_file:
    data = json.load(data_file)

obj = []

def make_scene(t, x):
    camera = Camera( 'location', [t*20,20,-x/1.5], 'look_at', [x/2,5,0])
    return Scene( camera, objects= obj, included=["glass.inc"])

def make_frame(t):
    #return scene.render("test.png", width=1024, height=512, antialiasing = 0.01, quality=100)
    return make_scene(t, 1).render(width=1024, height=512, antialiasing = 0.01, quality=100)

def render(data, length, x, y, z):
    if isinstance(data, list):
        print("X: " + str(x) + " Y: " + str(y) + " Z: " + str(z))
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1]))))
        for i,item in enumerate(data):
            if i == 0 or i == 1:
                new_y = (x + length) * (-i); new_x = x
            else:
                new_y = y; new_x = x + length
            print("X: " + str(x) + " Y: " + str(y) + " Z: " + str(z))
            obj.append(Cylinder([x,y,z], render(item, length, new_x, new_y, z), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4]))) # Das muss verändert werden xD

    elif data == 'h':
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1]))))
        print("X: " + str(x) + " Y: " + str(y) + " Z: " + str(z))
    else:
        raise ValueError
    return [x,y,z]

render(data, 100, 0, 0, 0)

obj.append(LightSource( [10, 120, -40], 'color', [1.3, 1.3, 1.3]))
obj.append(Background("color", [1,1,1]))

wall = Plane([0, 0, 1], 20, Texture(Pigment('color', [1, 1, 1])))
ground = Plane( [0, 1, 0], 0,
                Texture( Pigment( 'color', [1, 1, 1]),
                         Finish( 'phong', 0.1,
                                 'reflection',0.4,
                                 'metallic', 0.3)))

VideoClip(make_frame, duration=2).write_gif("anim.gif",fps=20)
