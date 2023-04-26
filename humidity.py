import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
DHT_READ_TIMEOUT = 5

def getSensorReadings():
    while True:
        result = {}
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        
        if humidity is not None and temperature is not None:
            result["Temperature"] = round(temperature,1)
            result["Humidity"] = round(humidity,1)
            return result
        else:
            DHT_READ_TIMEOUT
        