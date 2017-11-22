#!/usr/bin/env python3
# coding: utf8
# encoding=utf8
import os
import json
from plot import plot


def nameToJSON(name):
    os.chdir('../HcPlot-hs')
    os.system('stack build')
    HSdata = os.popen("stack exec create n '" + str(name) + "'").read()
    print("HS Data: " + str(HSdata))
    if(HSdata == ""):
        print("Fehlerhafter Name")
        #return False
    os.chdir('../python')
    try:
        #return json.loads(HSdata)
        return json.loads('["h", "h", "h", ["h","h",["h","h",["h","h",["h","h",["h","h","h"]]]]]]')
    except TypeError:
        print("Fehlerhafte JSON")
        return False


# plot(String name, Bool Animation)
plot(nameToJSON("2,4-dimethyl-hexan"), False)
