#!/usr/bin/env python3


from lights import CloudLights
l = CloudLights(44, self_brightness=0.25)

while True:
    l.random_callback_transitions(l.random_known_color)

