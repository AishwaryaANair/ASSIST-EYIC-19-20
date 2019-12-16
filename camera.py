from picamera import PiCamera
from time import sleep
import requests
#from google.cloud import storage
#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import db
while True:
    camera = PiCamera()

    camera.start_preview()
    sleep(5)

    camera.capture('/home/pi/Desktop/image.jpg')
    camera.stop_preview()
    camera.close()
    # Enable Storage

    url = "https://d554ba74.ngrok.io/IOT/Assist/saveImage.php"
    files = {'image': open('/home/pi/Desktop/image.jpg','rb')}
    try:
        response = requests.post(url,files = files, timeout= 60)
        print(response)
    except requests.exceptions.RequestException as e:
        print('Error: {}',format(e))
        print('timeout error')


'''
client = storage.Client()

# Reference an existing bucket.
bucket = client.get_bucket('assist-59664.appspot.com')

# Upload a local file to a new file to be created in your bucket.
zebraBlob = bucket.get_blob('image.jpg')
zebraBlob.upload_from_filename(filename='/home/pi/Desktop/image.jpg')
'''