
import RPi.GPIO as GPIO
import time

import random
import board
import time
import neopixel

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


RED = (255, 0, 0)
ORANGE = (245, 100, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
PINK = (255, 3, 183)
BLACK = (0, 0, 0)
white1 = (200,200,200)
white2 = (150,150,150)
white3 = (50,50,50)

green = (0,255,0)

colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK]

strip_pin = board.D21
strip_num_lights = 150
strip = neopixel.NeoPixel(strip_pin, strip_num_lights, brightness=1, auto_write=False)

DIRECTION = 1

def distance():
   
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
   
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
   
    StartTime = time.time()
    StopTime = time.time()
   
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()  

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


def idle(strip):
    for _ in range(2):
        time.sleep(.2)
        for i in range(strip_num_lights):
            if i%2 == 0:
                strip[i] = GREEN
            else:
                strip[i] = RED
        strip.show()    
        time.sleep(.2)
        for i in range(strip_num_lights):
            if i %2 == 0:
                strip[i] = RED
            else:
                strip[i] = GREEN
        strip.show()
def loading(strip,r,g,b):
   
    for i in range(9,strip_num_lights-9):
        strip.fill(BLACK)
def naughty_or_nice(strip,color):
    if color == "green":
        r = 0
        g = 200
        b = 0

    elif color == "red":
        r = 200
        g = 0
        b = 0
    direction = 1 
    strip.fill((r,g,b))
    strip.show()
    count = 0
    while count <3:
        if g == 255 or g == 50 or r == 255 or r == 50:
            direction *= -1
            count +=1
            #print(count) #optional to find count.
        if color == "green":
            g += direction
        elif color == "red":
            r += direction

        strip.fill((r,g,b))
        strip.show()
    strip.fill(BLACK)
    strip.show()

def check_status():
    #insert code for sensor
    #if "Sensor name" == "certain distence" (to not randomly go off)
        loading(strip,255,255,255)
        strip.fill(BLACK)
        strip.show()
        time.sleep(.5)

        color = random.choice(["red","green"])
        return color


 
if __name__ == '__main__':

#    while True:
#        idle(strip)
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)

            if distance() <= 40:
                print("Checking status...")
                color = check_status()
                naughty_or_nice(strip, color)
            else:
                idle(strip)

                # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        strip.fill(BLACK)
        strip.show()
        print("Measurement stopped by User")
        GPIO.cleanup()
