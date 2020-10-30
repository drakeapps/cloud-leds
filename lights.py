#!/usr/bin/env python3

#LED_COUNT = 100

import time
from random import randint
from random import choices

import board
import neopixel


class CloudLights:
    def __init__(self, led_count, brightness=1.0):
        self.pixels = neopixel.NeoPixel(board.D18, led_count, brightness=brightness)
        self.LED_COUNT = led_count
    
    def adjust_brightness(self, brightness):
        self.pixels =  neopixel.NeoPixel(board.D18, self.LED_COUNT, brightness=brightness)

    """
        lightning

        simulates lightning by quickly flashing a section of lights

        start: where lightning begins

        length: number of LEDs to flash

        flashes: number of flashes
            
    """
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
        # but we can transition to a randnom rainbow to a different rainbow 
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
    
    """
        random_noise

        returns a random 

        color_range: dictionary of min/max of RGB colors. omitted color is assumed to be 0. optional weights option, will use random.choices with weights passed through instead of randint
            example:
                {
                    red: {
                        min: 0
                        max: 5,
                        weights: [70, 70, 30, 20, 10]
                    },
                    blue: {
                        min: 0,
                        max: 40
                    }
                }

    """
    def random_noise(self, color):
        # there is a better way to do this, but im tired and can't think of it right now
        # just for speed, converting the object to a flat list to pass into rand int
        flat_colors = []
        weights = []
        for color_name in ('red', 'blue', 'green'):
            if color_name in color:
                flat_colors.append((color[color_name]["min"] if "min" in color[color_name] else 0))
                flat_colors.append((color[color_name]["max"] if "max" in color[color_name] else 0))
                weights.append(color[color_name]["weights"] if "weights" in color[color_name] else False)
            else:
                flat_colors.extend([0, 0])
                weights.append(False)
        lights = []
        for light in range(0,self.LED_COUNT):
            lights.append(
                (
                    choices(list(range(flat_colors[0], flat_colors[1]+1)), weights=weights[0])[0] if weights[0] else randint(*flat_colors[0:2]), 
                    choices(list(range(flat_colors[2], flat_colors[3]+1)), weights=weights[1])[0] if weights[1] else randint(*flat_colors[2:4]), 
                    choices(list(range(flat_colors[4], flat_colors[5]+1)), weights=weights[2])[0] if weights[2] else randint(*flat_colors[4:6])
                )
            )        
        return lights
    
    """
        off

        set all LEDS to 0,0,0 color aka turn the thing off

    """
    def off(self):
        self.pixels.fill((0,0,0))

