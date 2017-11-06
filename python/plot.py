#!/usr/bin/env python3
# coding: utf8
# encoding=utf8
from vapory import *
from moviepy.editor import VideoClip
import json
import tweepy
import numpy as np
import math, os, time, sys
from math import pi
from credentials import *
from convertBytes import convert_bytes

#sys.setdefaultencoding('utf8')

def backend(len, dep):
    os.chdir('../HcPlot-hs')
    os.system('stack build')
    #os.system('stack exec create ' + str(len) + ' ' + str(dep) + ' > data')
    # data = os.popen('stack exec create ' + str(len) + ' ' + str(dep)).read()
    os.chdir('../python')
    return json.loads(data)

def nameToJSON(name):
    os.chdir('../HcPlot-hs')
    os.system('stack build')
    HSdata = os.popen("stack exec create n '" + str(name) + "'").read()
    print("HS Data: " + str(HSdata))
    if(HSdata == ""):
        print("Fehlerhafter Name")
        return False
    os.chdir('../python')
    try:
        return json.loads(HSdata)
    except TypeError:
        print("Fehlerhafte JSON")
        return False

#data = backend(5, 2)


lange = 3 #sek. Länge der gif !!! must be int !!!
obj = []
x_cam = []
y_cam = []
z_cam = []
x_max = [0]
x_min = [0]
y_max = [0]
y_min = [0]

def make_scene(t, center):
    #camera = Camera( 'location', [t*50,20,-((x_max[0]+y_max[0])/1.25)], 'look_at', [x_max[0]/2,0,0])
    t = int(t*25)
    camera = Camera( 'location', [x_cam[t],y_cam[t],z_cam[t]], 'look_at', center)
    return Scene( camera, objects= obj, included=["glass.inc"])

def make_frame(t):
    #return scene.render("test.png", width=1024, height=512, antialiasing = 0.01, quality=100)
    center = ((x_max[0]+x_min[0])/2, (y_max[0]+y_min[0])/2, 0)
    return make_scene(t, center).render(width=1024, height=512, antialiasing = 0.01, quality=100)

def generate_circle(center=(0,0,0), r=50, n=100):
    return [
        (
            center[0] + (math.cos(2 * pi / n * x) * r),  # x
            center[1] + (math.sin(2 * pi / n * x) * r),  # y
            center[2] + (math.cos(2 * pi / n * x) * r)   # z

        ) for x in range(0, n + 1)]

def render(data, length, shrink, empty, x, y, z):
    if isinstance(data, list):
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1])))) # Create C node
        for i,item in enumerate(data): # Create New nodes around C
            [x_new, y_new, len_new, empty_new] = direct(len(data), length, shrink, empty, i, x, y, z)
            if(x_new > x_max[0]):
                x_max[0] = x_new
            if(x_new < x_min[0]):
                x_min[0] = x_new
            if(y_new > y_max[0]):
                y_max[0] = y_new
            if(y_new < y_min[0]):
                y_min[0] = y_new
            obj.append(Cylinder([x,y,z], render(item, len_new, shrink, empty_new, x_new, y_new, z), 0.3, Finish('ambient', 0.1, 'diffuse', 0.7), Pigment('color', [0.4,0.4,0.4])))
    elif data == 'h': # Create new h node
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.9,0.9,0.9]))))#White color
    return [x,y,z]

# Empty: 0 = left; 1 = up; 2 = right; 3 = down
def direct(datasize, length, shrink, empty, i, x, y, z):
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

def plot(data):
    print("Data: " + str(data))
    render(data, 15, 10, -1, 0, 0, 0)
    print("X max: " + str(x_max[0]) + ", Y max: " + str(y_max[0]))
    print("Kreispunkte: " + str(lange*25+1))
    center = ((x_max[0]+x_min[0])/2, (y_max[0]+y_min[0])/2, 0)

    print("Kreismitte: " + str(center))
    points = generate_circle(center=center, r=(x_max[0]+y_max[0]), n=lange*25+1)
    for x,y,z in points:
        x_cam.append(x)
        y_cam.append(z)
        z_cam.append(y)

    obj.append(LightSource( [10, 120, -40], 'color', [1.3, 1.3, 1.3]))
    obj.append(Background("color", [1,1,1]))

    VideoClip(make_frame, duration=lange).write_gif("animation.gif",fps=25)
    size = convert_bytes(os.stat("animation.gif").st_size)
    print("Filesize: " + size)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

running = True

while running:
    print("Listening Tweets...")
    tweets = api.search(q="@AlkanPlotter")
    for tweet in tweets:
        if "@AlkanPlotter" in tweet.text:
            user = tweet.user.screen_name
            #Entferne Username und Leerzeichen
            name = tweet.text.replace("@AlkanPlotter", "").replace(" ", "")
            print("Name von Twitter: " + str(name))
            data = nameToJSON(name)
            if(data):
                plot(data)
                api.update_with_media("animation.gif", "@" + user + " " + name, tweet.id)
                running = False
            else:
                print("Tweet ungultig!")
                running = False
