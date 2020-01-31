'''
Project Name: ASSIST
Author List: Aishwarya Nair, Shivani Patil, Prithvi Amin, Saily Natekar
Functions: distance(), distance3(), vibrate(), gpsInit(), GPS_Info(str), convert_to_degrees(str), distaneInit(), depthInit(), imageInit()
Global Variables: TRIGGER, ECHO, TRIGGER3, ECHO3, motor, gpgga_info, GPGGA_buffer, NMEA_buff, lat_in_degrees, long_in_degrees

'''
import RPi.GPIO as GPIO
import time
import requests
from time import sleep, time
import threading
from threading import Thread
import serial
import sys
from firebase import firebase
import cv2
from picamera import PiCamera
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
TRIGGER = 2
ECHO = 3
motor = 18
TRIGGER3 = 24                        #Associate pin 23 to TRIG
ECHO3 = 16
GPIO.setup(motor, GPIO.OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIGGER3 ,GPIO.OUT)
GPIO.setup(ECHO3, GPIO.IN)


'''
Function name: distance()
input: GPIO pin TRIGGER signal which is connected to Ultrasonic sensor
output: integer value of distance calculated with ultrasonic sensor (distance)
Logic: obtains start and stop time of the reflection of ultrasonic waves emitted from the sensor and divides it with the speed of 
sound to obtain the distance
Example Call: obstacle_distance = distance()

'''
def distance():
    
    GPIO.output(TRIGGER, True)
    
    sleep(1)
    GPIO.output(TRIGGER, False)
 
    StartTime = time()
    StopTime = time()
 
    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time()
 
    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance


'''
Function name: depth()
input: GPIO pin TRIGGER signal which is connected to Ultrasonic sensor
output: integer value of depth calculated with ultrasonic sensor (distance)
Logic: obtains start and stop time of the reflection of ultrasonic waves emitted from the sensor and divides it with the speed of 
sound to obtain the depth
Example Call: obstacle_depth = depth()

'''
def depth():
    
    GPIO.output(TRIGGER3, True)
    
    sleep(1)
    GPIO.output(TRIGGER3, False)
 
    StartTime = time()
    StopTime = time()
 
    # save StartTime
    while GPIO.input(ECHO3) == 0:
        StartTime = time()
 
    # save time of arrival
    while GPIO.input(ECHO3) == 1:
        StopTime = time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance


'''
Function name: vibrate()
input: None
output: High Signal of GPIO Pin connected to vibration motor
Logic: GPIO pin connected to the motor is sent a high signal to make the motor vibrate in case of obstacle
Example Call: vibrate()

'''

def vibrate():
    GPIO.output(motor, True)
    sleep(0.5)
    GPIO.output(motor, False)

gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyAMA0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0


'''
Function name: GPS_Info
input: NMEA buffer string
output: lat_in_degrees, long_in_degrees (setting global variables)
Logic: GPS module sends an NMEA Buffer string to the serial port ttyAMA0.
It then extracts the NMEA time, latitude and longitude that is sent to convert_to_degrees function to 
obtain the actual lattitude and longitde values
Example Call: GPS_Info([19,1283,2383,18383...])

'''


def GPS_Info(NMEA_buff):
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA strin
    lat = float(nmea_latitude)                  #convert string into float for calculation
    longi = float(nmea_longitude)               #convertr string into float for calculation
    
    lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format



'''
Function name: convert_to_degrees()
input: raw value of NMEA coordinates as obtained from GPS_Info
output: latitude/longitude in degrees
Logic: convert raw NMEA string into degree decimal format   
Example Call: convert_to_degrees(18353.2981)

'''

def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
    return position
    

'''
Function name: gpsInit()
input: getting raw serial port data
output: latitude/longitude in degrees and pushing it to database
Logic: obtain raw serial buffer data, extract GPGGA info string and NMEA buffer data 
and sending it to GPS_Info and convert_to_degrees function. The latitude and longitude thus obtained is sent to firebase.
Example Call: gpsInit()

'''

def gpsInit():
    while True:
        received_data = (str)(ser.readline())
        #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            GPS_Info(NMEA_buff)
            print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, '\n')
            app = firebase.FirebaseApplication('https://assist-42004.firebaseio.com')
            result = app.post('ASSIST', {'latitude':str(lat_in_degrees),'longitude':str(long_in_degrees)})
            print(result)

            

'''
Function name: distanceInit()
input: value of distance from distance function
output: None
Logic: obtain the values of the distance from the nearest obstacle and 
if the distance is less than 3ft/150 cm indicate with the vibration motor
Example Call: distanceInit()

'''
def distanceInit():
    dist = distance()
    print("dist:",dist)
    #sleep(0.5)
    while (dist<=150):
        print('distance obs')
        vibrate()
        sleep(0.2)
        break


'''
Function name: depthInit()
input: value of depth from depth function
output: None
Logic: obtain the values of the depth from the nearest obstacle and 
if the depth is greater than 50 cm indicate with the vibration motor
Example Call: depthInit()

'''        

def depthInit():
    depth = distance3()
    print("depth:",depth)
    #sleep(0.5)
    while (depth>=50):
        vibrate()
        sleep(0.2)
        break


'''
Function name: imageInit()
input: image from the pi Camera
output: image detected
Logic: getting trained class names from the model and reading the model file. 
Detecting the confidence level from each image and if confidence is greater than certain level then 
annotate the image. Send the detected class to firebase
Example Call: imageInit()

'''        

def imageInit():

    classNames = {0: 'background',
                  1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
                  7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
                  13: 'stop sign'}


    camera = PiCamera()

    camera.start_preview()
    sleep(1)

    camera.capture('image.jpeg')
    camera.stop_preview()
    camera.close()
    # Loading model
    model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                          'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')


    image = cv2.imread("image.jpeg")

    image_height, image_width, _ = image.shape

    model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
    output = model.forward()
    # print(output[0,0,:,:].shape)
     

    for detection in output[0, 0, :, :]:
        confidence = detection[2]
        if confidence > .5:
            class_id = detection[1]
            for key, value in classNames.items():
                if class_id == key:
                    class_name = value
            print(str(str(class_id) + " " + str(detection[2])  + " " + class_name))
            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height
            app = firebase.FirebaseApplication('https://assist-42004.firebaseio.com')
            result = app.post('ASSIST', {'image':str(class_name)})
            print(class_name)

'''
Function name: distanceThread()
input: None
output: None
Logic: Initiate the distance thread every second to detect incoming obstacles
Example Call: Thread(target = distanceThread).start

'''

def distanceThread():
    threading.Timer(1, distanceThread).start()
    distanceInit()

'''
Function name: depthThread()
input: None
output: None
Logic: Initiate the depth thread every second to detect incoming obstacles
Example Call: Thread(target = depthThread).start

'''
def depthThread():
    threading.Timer(1, depthThread).start()
    depthInit()

'''
Function name: gpsThread()
input: None
output: None
Logic: detect the location every 3 seconds 
Example Call: Thread(target = gpsThread).start

'''
def gpsThread():
    threading.Timer(3, gpsThread).start()
    gpsInit()


'''
Function name: imageThread()
input: None
output: None
Logic: starting the image processing thread every 3 seconds
Example Call: Thread(target = imageThread).start

'''
def imageThread():
    threading.Timer(3, imageThread).start()
    imageInit()
    
'''
Exceptions and exception handling
in cases gps and image processing fails to work
'''
try:
    if __name__ == '__main__':
        Thread(target = gpsThread).start()
        Thread(target = distanceThread).start
        Thread(target = depthThread).start()
        Thread(target = imageThread).start()
        
                                                 #get time, latitude, longitude
except KeyboardInterrupt:       #open current position information in google map
    GPIO.output(motor, False)
    sys.exit(0)
    GPIO.cleanup()

except Exception as e:
    print(e)
    while True:
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        depth = distance3()
        print ("Measured Depth = %.1f cm" % depth)
        sleep(0.50)
        if (dist<=50 or depth>=50):
            vibrate()











            
            
            




