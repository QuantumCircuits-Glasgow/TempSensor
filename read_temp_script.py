import os
import glob
import time
import threading
from pathlib import Path
from auto_email import send_autoemail

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'


temps=[]
files = []
for i in range(1, 3):
    temps.append(glob.glob(base_dir + '28*')[i])

device_file1 = device_folder1 + '/w1_slave'
device_file2 = device_folder2 + '/w1_slave'
temps_file = Path('temperatures.txt') #where the data is sent

auto_email = True #turn auto email feature on/off
threshold_temp = 35 #temperature above which an auto-email will be sent out


meas_time = 30 #how often the sensors take a measurement (seconds)
del_time = 604800 #how long a reading is saved (seconds) 604800s = 1 week

def read_temp_raw1():
    f = open(device_file1, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw2():
    f = open(device_file2, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp1():
    lines = read_temp_raw1()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw1()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def read_temp2():
    lines = read_temp_raw2()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw2()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
def write_temps():
    while True:
        if temps_file.exists() == False:
            x = open(temps_file, 'a')
            x.write('Sensor1(deg C), Sensor2(deg C), Date, Time \n')
            x.close
            
        else:           
            t = time.localtime()
            current_time = time.strftime("%d/%m/%y %H:%M:%S", t)
            temp_c1 = read_temp1()
            if temp_c1 >= threshold_temp and auto_email == True:
                send_autoemail(1, temp_c1, current_time)
            temp_c2 = read_temp2()
            if temp_c2 >= threshold_temp and auto_email == True:
                send_autoemail(2, temp_c2, current_time)
            
            x = open(temps_file, 'r')
            list_of_lines = x.readlines()
            x.close()
            list_of_lines.insert(1, '{}, {}, {}\n'.format(temp_c1, temp_c2, current_time))
            if len(list_of_lines) > del_time/meas_time:
                list_of_lines.pop()
            
            x = open(temps_file, 'w')
            x.writelines(list_of_lines)
            x.close()
            time.sleep(meas_time)
            
#def delete_temps():
#     while True:
#         time.sleep(del_time)
#         os.remove(temps_file)
        
write_temps()    
    
#t1 = threading.Thread(target=write_temps)
#t2 = threading.Thread(target=delete_temps)
#t1.start()
#t2.start()