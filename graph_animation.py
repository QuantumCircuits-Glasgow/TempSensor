import glob
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np

base_dir = '/sys/bus/w1/devices/'
device_folder1 = glob.glob(base_dir + '28*')[0]
device_folder2 = glob.glob(base_dir + '28*')[1]
device_file1 = device_folder1 + '/w1_slave'
device_file2 = device_folder2 + '/w1_slave'

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys1 = []
ys2 = []

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

# Generate random temp
def generate_temp():
    temperature = random.gauss(2050, 200)
    temperature = temperature/100        
    return temperature

# This function is called periodically from FuncAnimation
def animate(i, xs, ys1, ys2):

    # Read temperature
    temp_c1 = read_temp1()
    temp_c2 = read_temp2()

    # Add x and y to lists
    #xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    t = time.localtime()
    xs.append(time.strftime("%H:%M:%S", t))
    ys1.append(temp_c1)
    ys2.append(temp_c2)

    # Limit x and y lists to 60 items
    xs = xs[-300:]
    ys1 = ys1[-300:]
    ys2 = ys2[-300:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys1)
    ax.plot(xs, ys2)

    #Label x axis with every second timestamp to stop crowding
    xaxis_labels = xs
    for i in range(len(xaxis_labels)):
        if i%2 == 0:
            pass
        else:
            xaxis_labels[i] = ""
            
    # Format plot
    plt.xticks(xaxis_labels, rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Temperature over Time')
    plt.ylabel('Temperature (deg C)')
    
    
    

# Set up plot to call animate() function periodically

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys1, ys2), interval=5000)
plt.show()