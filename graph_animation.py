import glob
import time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import numpy as np
from types import SimpleNamespace

# from startup import read_temps


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
arr = [[], [], []]

# Generate random temp
def generate_temp(num):
    temps = []
    for _ in range(num):
        temperature = random.gauss(2050, 200)
        temperature = temperature / 100
        temps.append(temperature)
    return temps


# This function is called periodically from FuncAnimation
def animate(i, xs, arr):

    # Read temperature
    c1, c2, c3 = generate_temp(3)
    ys1, ys2, ys3 = arr

    # Add x and y to lists
    # xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    t = time.localtime()
    xs.append(time.strftime("%H:%M:%S", t))
    ys1.append(c1)
    ys2.append(c2)
    ys3.append(c3)

    arr = [ys1, ys2, ys3]

    # Limit x and y lists to 300 items
    xs = xs[-300:]
    ys1 = ys1[-300:]
    ys2 = ys2[-300:]
    ys3 = ys3[-300:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys1)
    ax.plot(xs, ys2)
    ax.plot(xs, ys3)
    plt.axhline(y=30, color="r", linestyle="-")

    # Label x axis with every second timestamp to stop crowding
    xaxis_labels = xs
    for i in range(len(xaxis_labels)):
        if i % 2 == 0:
            pass
        else:
            xaxis_labels[i] = ""

    # Format plot
    plt.xticks(xaxis_labels, rotation=45, ha="right")
    plt.subplots_adjust(bottom=0.30)
    plt.title("Temperature over Time")
    plt.ylabel("Temperature (deg C)")


# Set up plot to call animate() function periodically

ani = animation.FuncAnimation(fig, animate, fargs=(xs, arr), interval=5000)
plt.show()
