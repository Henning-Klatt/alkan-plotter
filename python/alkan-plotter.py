#!/usr/bin/env python3
# coding: utf8
# encoding=utf8

import json

from plot import Plot
from twitter import Twitter
from convertBytes import convert_bytes

data = json.loads('["h", "h", "h", ["h","h",["h","h",["h","h",["h","h",["h","h","h"]]]]]]')

p = Plot()
t = Twitter()

(username, tweetid, name) = t.listen()

p.plot(data, False)

t.reply(username, tweetid, name, data)
