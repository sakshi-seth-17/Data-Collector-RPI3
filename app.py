from picamera import PiCamera
import pyrebase
from datetime import datetime, timedelta
import os
from humidity import *
from userdefined import *
import time
from dht import *
import urllib.request
import firebase_admin
from firebase_admin import credentials, firestore
from sendEmail import *
from PIL import Image
#import paramiko
import json
import requests
import base64


cred = credentials.Certificate("/home/wendy-king/DataCollector/db-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


path = "/home/wendy-king/DataCollector/storage/"
configData = readJson("/home/wendy-king/DataCollector/config.json")
firebaseConfig = configData["firebaseConfig"]
storageBucket = configData["storageBucket"]
collectionName = configData["collection"]
rpidescription = "wendy-king"


'''
    Get IP address of the Raspberry Pi
'''
def raspberryIP():
    routes = json.loads(os.popen("ip -j -4 route").read())
    for r in routes:
        if r.get("dev") == "wlan0" and r.get("prefsrc"):
            ip = r["prefsrc"]
        break
    return ip
    
def brightness(image):
    # Open image using PIL
    img = Image.open(image).convert('L')
    # Calculate brightness
    hist = img.histogram()
    brightness = sum(i * hist[i] for i in range(256)) / (img.size[0] * img.size[1])
    return brightness
    
def storeOnWebserver(data):

    # Convert the JSON object to a string
    data_str = json.dumps(data)
    
    # Send the JSON string to the API endpoint
    response = requests.post('http://aspendb.uga.edu/firebase/getdata', json=data_str)


    
'''
    Save image to firebase storage
'''

def storeImage():
    try:
        firebase = pyrebase.initialize_app(firebaseConfig)
        storage = firebase.storage()
        camera = PiCamera()
        now = datetime.now()
        dt = now.strftime("%d-%m-%Y %H:%M:%S")
        name = dt+".jpg"
        camera.capture(name)
        storage.child("{}/{}".format(storageBucket,name)).put(name)
        brightness_value = brightness(name)
        
        configData["current_brightness"] = brightness_value
        flag = writeJson("/home/wendy-king/DataCollector/config.json",configData)
        
        with open(name, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        encoded_string = encoded_string.decode("utf-8")
        os.remove(name)
        camera.close()
        print("Image stored")
        
        return name.replace(".jpg",""), encoded_string
    except Exception as err:
        print("Error: ",err)
        return "",""

    
    
    
'''
    Store Humidity, Temperature, IP Address and Motion data in firebase database
'''
    
def storeKPI(docName,motion,encoded_string):
    data = getparams()  #Humidity and Temperature   
    location = ""
    try:
        doc_ref = db.collection("RPI-details")
        for doc in doc_ref.get():
            print(rpidescription)
            print(doc.id)
            if doc.id == rpidescription:
                location = doc.to_dict()["location"]
                break
    except:
        print("here")
        location = ""
        
    '''  if temperature is in abnormal range, check again and if still abnormal send an email '''
    if data["Temperature"] < 18 or  data["Temperature"] > 30: 
        data = getparams()
        if data["Temperature"] < 18 or  data["Temperature"] > 30: 
            sendStaus(rpidescription,location, raspberryIP(), data["Temperature"]) 
            
    data["Motion"] = motion   #Currently set to None
    data["Thermal"] = str(getThermal()) #Thermal matrix
    data["ImgRef"] = docName #ImgRef
    data["timestamp"] = docName#firestore.SERVER_TIMESTAMP #timestamp
    data["IPAddress"] = raspberryIP()   #IP address of the RPI
    data["brightness"] = configData["current_brightness"]   #store brightness
    data["rpi"] = "wendy_king"
    data["image"] = encoded_string
    data["location"]= location
    
    try:
        storeOnWebserver(data)
        doc_ref = db.collection(collectionName).document(docName)
        doc_ref.set(data)
        print("KPI stored")
    except Exception as err:
        print("Error: ",err)

motion = 0
while True:
    docName,encoded_string = storeImage()
    storeKPI(docName.replace(path,""),motion,encoded_string)
    #time.sleep(20)
    time.sleep(1800)

