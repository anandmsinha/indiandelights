import os
import sys
import re
import shuti1
import json
import cProfile
import random

li = ["dog dot", "do don't", "dumb-dumb", "no match"]

for element in li:
    m = re.match("(d\w+)\W(d\w+)", element)
    if m:
        print(m.groups())

for _, __ in enumerate(sys.path):
    shuti1.initialize('Hello', '!', 'HackerEarth')
    print __

while True:
    li_random = random.choice(li)
    print li_random
    if li[0] in li_random:
        break