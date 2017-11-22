from vapory import *
import numpy as np
import math, os, time, sys
from math import pi

class Plot:

    def __init__(self):
        self.obj = []

        self.x_max = [0]
        self.x_min = [0]
        self.y_max = [0]
        self.y_min = [0]

        self.x_cam = []
        self.y_cam = []
        self.z_cam = []

        self.lange = 3 #sek. Länge der gif !!! must be int !!!

    def make_scene(t, center):
        #camera = Camera( 'location', [t*50,20,-((self.x_max[0]+self.y_max[0])/1.25)], 'look_at', [self.x_max[0]/2,0,0])
        t = int(t*25)
        camera = Camera( 'location', [x_cam[t],y_cam[t],z_cam[t]], 'look_at', center)
        return Scene( camera, objects= obj, included=["glass.inc"])

    def make_frame(t):
        #return scene.render("test.png", width=1024, height=512, antialiasing = 0.01, quality=100)
        center = ((self.x_max[0]+self.x_min[0])/2, (self.y_max[0]+self.y_min[0])/2, 0)
        return make_scene(t, center).render(width=1024, height=512, antialiasing = 0.01, quality=100)

    def generate_circle(center=(0,0,0), r=50, n=100):
        return [
            (
                center[0] + (math.cos(2 * pi / n * x) * r),  # x
                center[1] + (math.sin(2 * pi / n * x) * r),  # y
                center[2] + (math.cos(2 * pi / n * x) * r)   # z

            ) for x in range(0, n + 1)]

    def render(self, data, length, shrink, empty, x, y, z):
        if isinstance(data, list):
            self.obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1])))) # Create C node
            for i,item in enumerate(data): # Create New nodes around C
                [x_new, y_new, len_new, empty_new] = self.direct(len(data), length, shrink, empty, i, x, y, z)
                if(x_new > self.x_max[0]):
                    self.x_max[0] = x_new
                if(x_new < self.x_min[0]):
                    self.x_min[0] = x_new
                if(y_new > self.y_max[0]):
                    self.y_max[0] = y_new
                if(y_new < self.y_min[0]):
                    self.y_min[0] = y_new
                self.obj.append(Cylinder([x,y,z], self.render(item, len_new, shrink, empty_new, x_new, y_new, z), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
        elif data == 'h': # Create new h node
            self.obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.9,0.9,0.9]))))#White color
        return [x,y,z]

    # Empty: 0 = left; 1 = up; 2 = right; 3 = down
    def direct(self, datasize, length, shrink, empty, i, x, y, z):
        if datasize != 0:
            if (i + empty) % 4 == 2:
                x_new = x + length; y_new = y
                len_new = length
                empty = 0 #Tested
            elif (i + empty) % 4 == 1:
                x_new = x; y_new = y + length
                len_new = length - shrink
                empty = 1 #Tested
            elif (i + empty) % 4 == 0: # Evtl swap with under
                x_new = x; y_new = y - length
                len_new = length - shrink
                empty = 2 #Tested
            elif (i + empty) % 4 == 3:
                x_new = x - length; y_new = y
                len_new = -length
                empty = 0 #2
        return [x_new, y_new, len_new, empty]

    def plot(self, data, animation):
        print("Data: " + str(data))
        self.render(data, 15, 10, -1, 0, 0, 0)
        print("X max: " + str(self.x_max[0]) + ", Y max: " + str(self.y_max[0]))
        print("Kreispunkte: " + str(self.lange*25+1))
        self.center = ((self.x_max[0]+self.x_min[0])/2, (self.y_max[0]+self.y_min[0])/2, 0)

        print("Kreismitte: " + str(self.center))

        self.obj.append(LightSource( [10, 120, -40], 'color', [1.3, 1.3, 1.3]))
        self.obj.append(Background("color", [1,1,1]))

        if(animation):
            from moviepy.editor import VideoClip
            points = generate_circle(center=center, r=(self.x_max[0]+self.y_max[0]), n=lange*25+1)
            for x,y,z in points:
                x_cam.append(x)
                y_cam.append(z)
                z_cam.append(y)

            VideoClip(make_frame, duration=lange).write_gif("animation.gif",fps=25)
            size = convert_bytes(os.stat("animation.gif").st_size)

        else:
            camera = Camera( 'location', [self.center[0],self.center[1],-(self.x_max[0]+self.y_max[0])/1.2], 'look_at', self.center)
            scene = Scene( camera, objects=self.obj, included=["glass.inc"])
            scene.render("image.png", width=3072, height=1536)
            #size = convert_bytes(os.stat("image.png").st_size)

        #print("Filesize: " + size)
