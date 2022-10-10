import os
import csv
import numpy as np
import csv
import shutil




def main():
    
    path = os.path.join(os.getcwd(), "DATA")
    maindata = open(os.path.join(path, "MainData.csv"), "a")
    writer = csv.writer(maindata)
    
    def reader(path):
        data_text = open(path, "r")
        data = list(csv.reader(data_text, delimiter=","))
        data.pop(0)
        data = np.array(data)
        date = str(data[0:,0]).split(" ")[0].replace("['","")
        times = data[:,0].tolist()
        for i in range(1, len(data[0])):
            column = data[:,i].astype(dtype=float)
            mean = np.mean(column)
            std = np.std(column)
            min_value = np.min(column)
            max_value = np.max(column)
            min_list = np.where(np.isin(column,min_value))[0].tolist()
            min_times = [str(times[i]).split(" ")[-1].replace("']","") for i in min_list]
            min_string = ",".join(list(dict.fromkeys(min_times))).rstrip()	
            max_list = np.where(np.isin(column,max_value))[0].tolist()
            max_times = [str(times[y]).split(" ")[-1].replace("']","") for y in max_list]
            max_string = ",".join(list(dict.fromkeys(max_times))).rstrip()
            pipe_data = [date, i, min_value, min_string, max_value, max_string, mean, std]
            
            writer.writerow(pipe_data)


    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file != "MainData.csv":
            reader(os.path.join(path, file))
            print("Written File Data", file)
            shutil.move(os.path.join(path, file), os.path.join(path, "Loaded", file))	
