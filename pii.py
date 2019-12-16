#Libraries
import RPi.GPIO as GPIO
import time
import requests
from time import sleep, time

#GPIO Mode (BOARD / BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
sleep(2)
'''
GPIO_PWM = 14
GPIO_IN = 17
GPIO_OUT = 4
'''
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
#GPIO.setup(GPIO_PWM,GPIO.IN)
#GPIO.setup(GPIO_IN, GPIO.IN)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    sleep(1)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time()
    StopTime = time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

'''
def calculate_vibration(distance):
    trig.on()
    sleep(1)
    trig.off()
    print(distance)
    if (distance <= 150):
        vibration=0;
    else:
        vibration = (-(distance - 0.2) / (3.98)) + 1;
    print(vibration)
    return vibration

def get_pulse_time():
    trig.on()
    sleep(0.001)
    trig.off()

    while echo.is_active == False:
        pulse_start = time()

    while echo.is_active == True:
        pulse_end = time()

    sleep(0.06)

    try:
        return pulse_end - pulse_start
    except:
        return 0.02
'''
    
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            sleep(1)
            text = {'distance': dist}
            #vibration = calculate_vibration(dist)
            #motor.value = vibration


            #url = 'https://79da74ba.ngrok.io/IOT/index.php'
            
            r = requests.post('https://d554ba74.ngrok.io/IOT/Assist/index1.php',text)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()