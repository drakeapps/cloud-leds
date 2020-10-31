#!/usr/bin/env python3


import time
from random import randint
from random import choices
import random

import board
import neopixel


class CloudLights:
    def __init__(self, led_count, brightness=1.0, self_brightness=1.0):
        self.pixels = neopixel.NeoPixel(board.D18, led_count, brightness=brightness)
        self.brightness = self_brightness
        self.LED_COUNT = led_count
    
    def set_self_brightness(self, brightness):
        """
            set the brightness level adjustment for the automated
            color functions. instead of setting a brightness on the strip,
            which is questionable at working, this sets the multiplier we
            use to set the color levels

            so brightness of 0.1 will cause RGB (255, 255, 255) to become
            (25, 25, 25) making it effectively 10% brightness

            use self.fixcolor([0-255]) to adjust full color down to brightness levels
            TODO: wrapper for writing the colors

            brightness: 0.0-1.0 value
        """
        self.brightness = brightness


    def adjust_brightness(self, brightness):
        """
            recreates neopixel object with new brightness value
            (may not work correctly)

            brightness: 0.0-1.0 value for brightness
        """
        self.pixels =  neopixel.NeoPixel(board.D18, self.LED_COUNT, brightness=brightness)
    
    def fixcolor(self, color, brightness=None):
        if not brightness:
            brightness = self.brightness
        return round(color * brightness)

    def lightning(self, start=0, length=10, flashes=5, brightness=None):
        """
            simulates lightning by quickly flashing a section of lights

            start: where lightning begins

            length: number of LEDs to flash

            flashes: number of flashes

            brightness: 0-1 value to override the self_brightness level
                
        """
        
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
            lights.append((self.fixcolor(255, brightness=brightness), self.fixcolor(255, brightness=brightness), self.fixcolor(255, brightness=brightness)))
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
        random_lightning

        callback for transitions to add a random bit of flashing 
        to be shown to simulate lightning

        chances: 1 in chances amount to do the lightning

    """
    def random_lightning(self, chances=10000):
        if randint(0,chances) == 0:
            amount = randint(5,15)
            start = randint(0, self.LED_COUNT- amount)
            flashes = randint(3,7)
            self.lightning(start=start, length=amount, flashes=flashes)


    """
        transition

        color: tuple of RGB colors to transition all LEDs too

        length: seconds to transition to that color
            default: 60

        interval:
            seconds between color changes
            default: 0.05

    """
    def transition(self, color=(0,0,0), length=60, interval=0.05, step_callback=None):
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


    def random_callback_transitions(self, color_callback, length=15, interval=0.4, lightning_chances=None, step_callback=None):
        """
        randomly transitions to colors based on callback passed down

        note: I don't actually know if this is needed, it's kinda just wrapping the transition callback
            it kinda makes it easier to 

        :param lightning_chances: 1 in chances for lightning to occur
        """
        if step_callback:
            callback = step_callback
        elif lightning_chances:
            callback = lambda x:  x.random_lightning(chances=lightning_chances)
        else:
            callback = lambda x: None
        self.transition(color_callback, length=15, interval=0.4, step_callback=callback)
    

    def random_solid_color (self):
        return (randint(0,self.fixcolor(255)), randint(0,self.fixcolor(255)), randint(0,self.fixcolor(255)))

    def random_known_color (self, color=None):
        colors = {
            'red':      (255, 0, 0),
            'green':    (0, 255, 0),
            'blue':     (0, 0, 255),
            'yellow':   (255, 255, 0),
            'orange':   (255, 128, 0),
            'cerulean': (255, 255, 0),
            'purple':   (128, 0, 255),
            'pink':     (255, 0, 255)
        }

        return random.choice(list(colors.values()))