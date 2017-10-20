from vapory import *
from moviepy.editor import VideoClip
import json
import tweepy
from credentials import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

with open('data.json') as data_file:
    data = json.load(data_file)

obj = []

def make_scene(t, x):
    camera = Camera( 'location', [20,20,-40], 'look_at', [0,0,0])
    return Scene( camera, objects= obj, included=["glass.inc"])

def make_frame(t):
    #return scene.render("test.png", width=1024, height=512, antialiasing = 0.01, quality=100)
    return make_scene(t, 1).render(width=1024, height=512, antialiasing = 0.01, quality=100)

def render(data, length, shrink, empty, x, y, z):
    if isinstance(data, list):
        obj.append(Sphere([x, y, z], 2, Texture(Pigment('color', [0.1,0.1,0.1])))) # Create C node
        for i,item in enumerate(data): # Create New nodes around C
            [x_new, y_new, len_new, empty_new] = direct(len(data), length, shrink, empty, i, x, y, z)
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

render(data, 15, 10, -1, 0, 0, 0)

obj.append(LightSource( [10, 120, -40], 'color', [1.3, 1.3, 1.3]))
obj.append(Background("color", [1,1,1]))

VideoClip(make_frame, duration=1).write_gif("anim.gif",fps=1)
api.update_with_media("anim.gif", "Haskell Foreign Function Interface fehlt. lol.")
