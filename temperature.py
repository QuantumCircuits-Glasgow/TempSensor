import os
import glob
import time
from datetime import date, datetime
import csv
import schedule
import load_daily_data
# from ISStreamer.Streamer import Streamer

# streamer = Streamer(bucket_name="Temperature Stream", bucket_key="piot_temp_stream031815", access_key="ist_OTZrHA34ggIFjpWSdXcIazgXf4w5G69B")

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

numberSensors = 3
broken = False

base_dir = '/sys/bus/w1/devices/'
sensors_folders = []
sensors = []

sensors_text = open("./sensors.txt", "r")
placed_sensors = {sensor.rstrip().split(": ")[0]:sensor.rstrip().split(": ")[-1] for sensor in sensors_text.readlines() if sensor != ""}
sensors_text.close()
   

try:
    for i in range(numberSensors):
        device_folder = glob.glob(base_dir + '28*')[i]
        device = device_folder.split("/")[-1]
        sensors.append(device)
        sensors_folders.append(device_folder + '/w1_slave')
except IndexError:
    broken = True
    print("One or more sensors have not been detected")
    print("Running Diagnostic")
    
    
if len(placed_sensors) < numberSensors:
    print("Additional Sensors Detected")
    sensors_text = open("./sensors.txt", "w")
    for i in range(len(placed_sensors), numberSensors):
        sensors_text.write(f"Sensor{i+1}: {sensors[i]}\n")
    sensors_text.close()
           
    
# Checking if all sensors are present:
broken_sensors = list(placed_sensors.values())
new_sensors = []
for i, device in enumerate(sensors):    
    if device in placed_sensors.values():
        broken_sensors.remove(device)
        print(f"Sensor{i+ 1} DETECTED: {device}")
    else:
        new_sensors.append(device)

for i, device in enumerate(broken_sensors): 
    broken = True 
    sensor_value = list(placed_sensors.keys())[list(placed_sensors.values()).index(device)]         
    print(f"###ERROR###\n{sensor_value} : {device} was not detected")
    if len(new_sensor) != 0:
        check = input(f"Did you replace this sensor with: {new_sensors[i]}? [y/N] ")
        if check.lower() == "y":
            placed_sensors[sensor_value] = new_sensors[i]
        else:
            new_sensor = input("Please manually enter the serial number: ")
            placed_sensors[sensor_value] = new_sensor
    else:
        print("New sensor required!")
        check = input(f"Do you wish to continue with broken sensor? [y/N] ")

if broken:
    sensors_text = open("./sensors.txt", "w")
    for sensor, serial in placed_sensors.items():
        sensors_text.write(f"{sensor}: {serial}\n")
    sensors_text.close()

def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensor):
    lines = read_temp_raw(sensor)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

#Creating CSV file where this dates data will be written:
today = date.today()

try:
    csv_file = open(f"DATA//DATA:{today}.csv", "x")
    writer = csv.writer(csv_file)
    headings = [f"Pipe {i + 1}" for i in range(numberSensors)]
    headings.insert(0, "Date & Time")
    writer.writerow(headings)
except FileExistsError:
    csv_file = open(f"DATA//DATA:{today}.csv", "a", newline="\n")
    writer = csv.writer(csv_file)
    
    
try:
    schedule.every().day.at("06:00").do(load_daily_data.main())
except:
    print("Unable to schedule file upload, will attempt in 6 hours again")


while True:    
    temps = [f"{datetime.now()}".split(".")[0]] 
       
    for i, sensor_folder in enumerate(sensors_folders):
        sensor = sensor_folder.split("/")[-2]
        temp_c = read_temp(sensor_folder)
        print(f"Pipe {list(placed_sensors.values()).index(sensor) + 1}", temp_c)
        # streamer.log(f"temperature of sensors {i+1} (C)", temp_c)
        temps.append(temp_c)
        
    print("#" * 50)    
    writer.writerow(temps)
    schedule.run_pending()    
    time.sleep(60)
