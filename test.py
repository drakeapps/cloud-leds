#!/usr/bin/env python3

import random


def random_lightning(lights, chances=10000):
    print(f"called {chances}")
    if random.randint(0,chances) == 0:
        amount = random.randint(5,15)
        start = random.randint(0, lights.LED_COUNT- amount)
        flashes = random.randint(3,7)
        lights.lightning(start=start, length=amount, flashes=flashes)

from lights import CloudLights
l = CloudLights(300)
#l.lightning()
#print(l.pixels[0])
while True:
    callback = lambda x:  random_lightning(x, 100)
    l.transition((random.randint(0,25),random.randint(0,25),random.randint(0,25)), length=15, interval=0.4, step_callback=callback)

