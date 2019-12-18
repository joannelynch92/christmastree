#!/usr/bin/env python3

# Each pixel cycles through RGB wheel at random speed

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

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def wheeler():
    slowness = random.randrange(1, 10)
    while True:
        for pos in range(255):
            for i in range(slowness):
                yield(wheel(pos))

def dowheel(strip, wait_ms=50):
    wheelers = [wheeler() for i in range(strip.numPixels())]
    while True:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, next(wheelers[i]))
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
            print('Random wheel')
            dowheel(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
