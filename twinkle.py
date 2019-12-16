#!/usr/bin/env python3

# Light all pixels at a fraction of max and randomly pulse to max for
# twinkle effect.

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

def twinkler():
    base_brightness = int(LED_BRIGHTNESS/4)
    delta_brightness = LED_BRIGHTNESS - base_brightness
    while True:
        for i in range(10):
            c = base_brightness + int(delta_brightness/10.0*i)
            yield Color(c, c, c)
        for i in range(9, -1, -1):
            c = base_brightness + int(delta_brightness/10.0*i)
            yield Color(c, c, c)
        for i in range(int(random.random()*300)):
            yield Color(base_brightness, base_brightness, base_brightness)

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
            print('Twinkle')
            twinkle(strip)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
