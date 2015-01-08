import sys
import collections
import math

from collections import Counter

class HackerEarth(object):
    def __init__(self, name, role, hobby):
        self.name = name
        self.role = role
        self.hobby = hobby

    def print_details(self):
        print "Name:", self.name
        print "Role:", self.role
        print "Hobby:", self.hobby

cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    cnt[word] += 1

def initialize(greet, character, company):
    print greet, character, company

