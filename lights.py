#!/usr/bin/env python3

#LED_COUNT = 100

import time

import board
import neopixel


class CloudLights:
    def __init__(self, led_count, brightness=1.0):
        self.pixels = neopixel.NeoPixel(board.D18, led_count, brightness=brightness)
        self.LED_COUNT = led_count

    def lightning(self, start=0, length=10, flashes=5):
        current = start
        end = current + length

        #for i in range(current, end):
        #    self.pixels[i] = (255,255,255)
        #    time.sleep(0.01)
        #time.sleep(0.05)

        original = []
        lights = []
        dark = []
        for i in range(current, end):
            original.append(self.pixels[i])
        for i in range(0,length):
            lights.append((255,255,255))
            dark.append((0,0,0))
            

        for i in range(0,flashes):
            #for j in range(current,end):
            #    self.pixels[j] = (0,0,0)
            self.pixels[current:end] = lights
            time.sleep(0.01)
            #for j in range(current,end):
            #    self.pixels[j] = (255,255,255)
            self.pixels[current:end] = dark
            time.sleep(0.03)
        self.pixels[current:end] = original
        #for i in range(current, end):
        #    self.pixels[i] = (0,0,0)
        #    time.sleep(0.01)

    """
        transition

        color: tuple of RGB colors to transition all LEDs too

        length: seconds to transition to that color
            default: 60

        interval:
            seconds between color changes
            default: 0.05

    """
    def transition(self, color, length=60, interval=0.05, step_callback=None):
        # this isn't effecient when talking about memory consumption
        # but we can transition 
        steps = int(length / interval)
        (red, green, blue) = color
        transitions = []
        for i in range(0, steps):
            transitions.append([])
        for i in range(0, self.LED_COUNT):
            initial = self.pixels[i]
            transitions.append([])
            (init_red, init_green, init_blue) = initial
            step_red = (red - init_red) / steps
            step_green = (green - init_green) / steps
            step_blue = (blue - init_blue) / steps
            for j in range(0,steps):
                init_red += step_red
                init_green += step_green
                init_blue += step_blue
                transitions[j].append((init_red, init_green, init_blue))

        for i in range(0,steps):
            print(f"step: {i}")
            start_time = time.time()
            self.pixels[0:] = transitions[i]
            if step_callback:
                step_callback(self)
            now = time.time()
            print(f"now: {now} start_time: {start_time} interval: {interval}")
            if now < start_time + interval:
                time.sleep(interval - (now - start_time))



