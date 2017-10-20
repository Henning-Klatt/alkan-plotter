from vapory import *
import json
from pprint import pprint
from moviepy.editor import VideoClip

with open('data.json') as data_file:
    data = json.load(data_file)

obj = []

c = [0]
c[0] += 1
h = [0]

def make_scene(t):
    camera = Camera( 'location', [t*20,20,-x/1.5], 'look_at', [x/2,5,0])
    return Scene( camera, objects= obj, included=["glass.inc"])

def make_frame(t):
    #return scene.render("test.png", width=1024, height=512, antialiasing = 0.01, quality=100)
    return make_scene(t).render(width=1024, height=512, antialiasing = 0.01, quality=100)


def getArrays(data, arrays):
    for i in data:
        if(isinstance(i, list)):
            c[0] += 1
            getArrays(i, arrays)
        else:
            h[0] += 1
    return arrays

def render(data, length, x, y, z):
    if isinstance(data, list):
        obj.append(Shpere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1]))))
        # Foreach element
        obj.append(Cylinder([x,y,z], render(?,?,?,?), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4]))) # Das muss verändert werden xD
    else:
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1]))))

getArrays(data, 0)

print("Arrays: " + str(c[0]))
print("H's am Main: " + str(h[0]))

x = 0
y = 0
for index in range(c[0]):
    x += 10
    obj.append(Sphere([x, 0, 2], 2, Texture( Pigment('color', [0.1,0.1,0.1]))))
    obj.append(Sphere([x, 10, 2], 1.5, Texture(Pigment('color', [0.9,0.9,0.9]))))
    obj.append(Sphere([x, -10, 2], 1.5, Texture(Pigment('color', [0.9,0.9,0.9]))))
    obj.append(Cylinder((x, -10, 2), (x, 10, 2), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
    if(x/10 != c[0]):
        obj.append(Cylinder((x, 0, 2), (x+12, 0, 2), 0.5, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
    else:
        obj.append(Sphere([x+10, 0, 2], 2, Texture(Pigment('color', [0.9,0.9,0.9]))))
        obj.append(Cylinder((x, 0, 2), (x+10, 0, 2), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
    if(x/10 == 1):
        obj.append(Sphere([x-10, 0, 2], 1.5, Texture(Pigment('color', [0.9,0.9,0.9]))))
        obj.append(Cylinder((x-10, 0, 2), (x, 0, 2), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))


#for index in range(mainAtoms):
#    if(isinstance(data[index], list)):
#        for i in data[index]:
#            x = x + 10
#            obj.append(Sphere([x,3,2], 2, Texture( Pigment('color', [0.1,0.1,0.1]))))
#            c = c+1
#            if(index != c):
#                obj.append(Cylinder((x, 3, 2), (x+12, 3, 2), 0.5, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
#            print(i)
            #if(isinstance(i, list)):

        #obj.append(Sphere([x,3,2], 2, Texture( Pigment('color', [0.1,0.1,0.1]))))
    #if(index+1 != mainAtoms):
    #    obj.append(Cylinder((x, 3, 2), (x+12, 3, 2), 0.5, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))

#Links/rechts - hoch/runter - vorne/hinten

obj.append(LightSource( [10, 120, -40], 'color', [1.3, 1.3, 1.3]))
obj.append(Background("color", [1,1,1]))

wall = Plane([0, 0, 1], 20, Texture(Pigment('color', [1, 1, 1])))
ground = Plane( [0, 1, 0], 0,
                Texture( Pigment( 'color', [1, 1, 1]),
                         Finish( 'phong', 0.1,
                                 'reflection',0.4,
                                 'metallic', 0.3)))

VideoClip(make_frame, duration=2).write_gif("anim.gif",fps=20)
