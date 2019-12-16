#!/usr/bin/env python3

# Light all pixels at a fraction of max and randomly pulse to max for
# twinkle effect.

import itertools
import random
import time
from rpi_ws281x import PixelStrip, Color
import argparse

# LED strip configuration:
LED_COUNT = 90        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

BASE_BRIGHTNESS = int(LED_BRIGHTNESS/4)
TINT_BRIGHTNESS = BASE_BRIGHTNESS
DELTA_BRIGHTNESS = LED_BRIGHTNESS - BASE_BRIGHTNESS

def twinkler():
    """A generator that mostly yields a base colour but with random twinkles"""
    base = (
        BASE_BRIGHTNESS + random.randrange(TINT_BRIGHTNESS),
        BASE_BRIGHTNESS + random.randrange(TINT_BRIGHTNESS), 
        BASE_BRIGHTNESS + random.randrange(TINT_BRIGHTNESS)
    )
    basec = Color(*base)
    while True:
        # Random dwell on base colour.
        for i in range(int(random.random()*300)):
            yield basec
        # Jump to white brightness of brightest tint and
        # sweep from 0 - 10 - 0
        start = max(base)
        pulse = LED_BRIGHTNESS - start
        for i in itertools.chain(range(10), range(9, -1, -1)):
            d = int(pulse/10.0*i)
            yield Color(start+d, start+d, start+d)

def twinkle(strip, wait_ms=50):
    twinklers = [twinkler() for i in range(strip.numPixels())]
    while True:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, next(twinklers[i]))
        strip.show()
        time.sleep(wait_ms / 1000.0)

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print('Pastel twinkle')
            twinkle(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
