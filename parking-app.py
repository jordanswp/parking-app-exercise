import tkinter as tk
from tkinter import filedialog
import math
import sys
import os

#what if uploaded file is in a different structure, like comma
#1 function for reading the file
#1 function for reading the lines
#1 function for handling entering of vehicles
#1 function for handling exiting of vehicles
#split file into different functions
#repeated twice (car enters twice)
# in readme file, brief desaription of how the dictionary is structured, write down what empty, empty is.
#invalid scenario: no timestamp. and no carplate. both none. 
# Function to count total number of lots for both car and motorcycle. e.g. count total number of keys in car dictionary, either that or get the length
# parking_lots = {
#     "car" : {
#         "CarLot0": {},
#         "CarLot1": {}, 
#     }
# }
# parking lot dictionary and just have separate dictionaries 
# parking_lots = {
#     "CarLot0": {},
#     "CarLot1": {}, 
# }

root = tk.Tk()
root.withdraw()

print('Please select a file.')

#upload file, only .txt files 
uploaded_file = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")]) 

try:
    f = open(uploaded_file, 'r')
except FileNotFoundError:
    print("No file uploaded. Please try again.")
    sys.exit()

#read file
if os.stat(uploaded_file).st_size == 0:
    print('File is empty. Please upload another file.')
    sys.exit()
else:
    file1 = f.readlines()


#initialise parking lot dict
parking_lots = {
    "car": {},
    "motorcycle": {}
}

car_lot = parking_lots["car"]
motorcycle_lot = parking_lots["motorcycle"]

for i, line in enumerate(file1):
    _data = line.split()
    if i == 0:
        #if first line is not empty
        if line:
            try:
                #determine total number of car and motorcycle parking lots
                total_car_lots = int(_data[0])
                total_motorcycle_lots = int(_data[1])
            except ValueError:
                print("No available parking lots indicated. Please check file and try again.")
                sys.exit()
        else:
            print("No available parking lots indicated. Please check file and try again.")
            sys.exit()


        count = 1

        if (total_car_lots >= 1 and total_motorcycle_lots >= 1):

            #create dictionary according to respective parking lot size
            while count <= total_car_lots:
                car_lot["CarLot" + str(count)] = ["empty", "empty"]
                count += 1

            else: 
                #reset count back to 1
                count = 1

            while count <= total_motorcycle_lots:
                motorcycle_lot["MotorcycleLot" + str(count)] = ["empty", "empty"]
                count += 1

        #if there is no car lots
        elif (total_car_lots == 1 and total_motorcycle_lots > 1):
            car_lot["CarLot"] = ["null", "null"]

            while count < total_motorcycle_lots:
                motorcycle_lot["MotorcycleLot" + str(count)] = ["empty", "empty"]
                count += 1

        #if there is no motorcycle lots
        elif (total_motorcycle_lots == 1 and total_car_lots > 1):
            motorcycle_lot["MotorcycleLot"] = ["null", "null"]

            while count < total_car_lots:
                car_lot["CarLot" + str(count)] = ["empty", "empty"]
                count += 1

        #if there is no lots
        elif (total_car_lots == 1 and total_motorcycle_lots == 1):
            motorcycle_lot["MotorcycleLot"] = ["empty", "empty"]
            car_lot["CarLot"] = ["empty", "empty"]

        else:
            print("No available parking lots indicated. Please check file and try again.")
            sys.exit()

    else:
        #if line is not empty
        if _data:
            mode = _data[0]
        else:
            break
        
        if mode == "Enter":
            vehicle = _data[1]
            num_plate = _data[2]
            time_stamp = _data[3]

            #check if car
            if vehicle == "car":
                #check car lot availability
                for lot_num, avail in car_lot.items():

                    if avail == ["empty", "empty"]:
                        #fill up car lot
                        car_lot[lot_num] = [num_plate, time_stamp]
                        print("Accept {}".format(lot_num))
                        break

                    #if no available car lot
                    elif ["empty", "empty"] not in car_lot.values():
                        print('Reject')
                        break

            #check if motorcycle
            elif vehicle == "motorcycle":
                #check motorcycle lot availability
                for lot_num, avail in motorcycle_lot.items():

                    if avail == ["empty", "empty"]:
                        #fill up motorcycle lot
                        motorcycle_lot[lot_num] = [num_plate, time_stamp]
                        print("Accept {}".format(lot_num))
                        break

                    #if no available motorcycle lot
                    elif ["empty", "empty"] not in motorcycle_lot.values():
                        print('Reject')
                        break
            else:
                print('Invalid vehicle type. Please check file contents and try again.')
                # break
            
        elif mode == "Exit":
            num_plate = _data[1]
            time_stamp = _data[2]
            car_price = 2
            motorcycle_price = 1


            car_lot_detail, car_lot_timestamp = zip(*car_lot.values())
            motorcycle_lot_detail, motorcycle_lot_timestamp = zip(*motorcycle_lot.values())

            #if exiting vehicle is a car
            if num_plate in car_lot_detail:
                for lot_num, details in car_lot.items():
                    #if exiting number plate matches a record in car lots
                    if details[0] ==  num_plate:

                        #free up lot
                        car_lot[lot_num] = ["empty", "empty"]

                        #calculate price
                        try:
                            total_mins_parked = (int(time_stamp) - int(details[1]))/60
                            total_hours_parked = math.ceil( total_mins_parked / 60 )
                            total_cost = ( total_hours_parked * car_price )
                            print("{} {}".format(lot_num, total_cost))
                        except ValueError:
                            print('Invalid timestamp detected. Please check file contents and try again.')
                        break

            #if exiting vehicle is a motorcycle
            elif num_plate in motorcycle_lot_detail:
                for lot_num, details in motorcycle_lot.items():
                    #if exiting number plate matches a record in motorcycle lots
                    if details[0] ==  num_plate:

                        #free up lot
                        motorcycle_lot[lot_num] = ["empty", "empty"]

                        #calculate price
                        try:
                            total_mins_parked = (int(time_stamp) - int(details[1]))/60
                            total_hours_parked = math.ceil( total_mins_parked / 60 )
                            total_cost = ( total_hours_parked * motorcycle_price )
                            print("{} {}".format(lot_num, total_cost))
                        except ValueError:
                            print('Invalid timestamp detected. Please check file contents and try again.')
                        break
            else:
                #if exiting vehicle does not match any record
                print("Vehicle does not exist in carpark.")
                # break
        else:
            print("Invalid mode detected. Please check file contents and try again.")

        

f.close()
