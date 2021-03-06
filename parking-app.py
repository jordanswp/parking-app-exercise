import tkinter as tk
from tkinter import filedialog
import math
import sys
import os

def upload_file():
    root = tk.Tk()
    root.withdraw()

    print('Please select a file.')

    #upload only .txt files
    uploaded_file = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])

    #additional check to ensure only .txt files may be uploaded
    if not uploaded_file.endswith(".txt"):
        print("Incorrect fie format detected. Only .txt files may be uploaded.")
        sys.exit()


    try:
        f = open(uploaded_file, "r")
    except FileNotFoundError:
        print("No file uploaded. Please try again.")
        sys.exit()

    if os.stat(uploaded_file).st_size == 0:
        print('File is empty. Please upload another file.')
        sys.exit()

    return f

def read_file():
    f = upload_file()

    read_file = f.readlines()
    return read_file

input_file = read_file()

def create_carpark():

    #initialise parking lot dict
    parking_lots = {
        "car": {},
        "motorcycle": {}
    }

    car_lot = parking_lots["car"]
    motorcycle_lot = parking_lots["motorcycle"]    

    # Get the parking lots available
    for i, line in enumerate(input_file):
        _data = line.split()
        if i == 0: 
            #if first line is not empty
            if line:
                try:
                    #determine total number of car and motorcycle parking lots
                    total_car_lots = int(_data[0])
                    total_motorcycle_lots = int(_data[1])
                except ValueError:
                    print("Invalid value detected for lot space. Please check file and try again.")
                    sys.exit()
                except IndexError:
                    print("No available parking lots indicated. Please check file and try again.")
                    sys.exit()
            else:
                print("Invalid parking lots indicated. Please check file and try again.")
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

    # no motorcycle lots and car lots
    elif (total_car_lots == 1 and total_motorcycle_lots == 1):
        motorcycle_lot["MotorcycleLot"] = ["empty", "empty"]
        car_lot["CarLot"] = ["empty", "empty"]

    else:
        print("No available parking lots indicated. Please check file and try again.")
        sys.exit()

    return parking_lots

parking_lots = create_carpark()
car_lot = parking_lots["car"]
motorcycle_lot = parking_lots["motorcycle"]

def vehicle_enter(line):
    _data = line.split()
    try:
        vehicle = _data[1]
        num_plate = _data[2]
        timestamp = _data[3]
    except IndexError:
        print("Missing data detected. Please check file.")
        sys.exit()

    if vehicle == "car":
        #check car lot availability
        for lot_num, status in car_lot.items():
            if status == ["empty", "empty"]:
                #fill up car lot
                car_lot[lot_num] = [num_plate, timestamp]
                print("Accept {}".format(lot_num))
                break
            #if no available car lot
            elif ["empty", "empty"] not in car_lot.values():
                print('Reject')
                break

    elif vehicle == "motorcycle":
        #check car lot availability
        for lot_num, status in motorcycle_lot.items():
            if status == ["empty", "empty"]:
                #fill up motorcycle lot
                motorcycle_lot[lot_num] = [num_plate, timestamp]
                print("Accept {}".format(lot_num))
                break

            #if no available motorcycle_lot lot
            elif ["empty", "empty"] not in motorcycle_lot.values():
                print('Reject')
                break
    else:
        print('Invalid vehicle type. Please check file contents and try again.')
        # break
    
def calculate_car_price(timestamp, exit_timestamp, car_price, lot_num):
        total_mins_parked = (int(timestamp) - int(exit_timestamp))/60
        total_hours_parked = math.ceil( total_mins_parked / 60 )
        total_cost = ( total_hours_parked * car_price )
        print("{} {}".format(lot_num, total_cost))

def calculate_motorcycle_price(timestamp, exit_timestamp, motorcycle_price, lot_num):
        total_mins_parked = (int(timestamp) - int(exit_timestamp))/60
        total_hours_parked = math.ceil( total_mins_parked / 60 )
        total_cost = ( total_hours_parked * motorcycle_price )
        print("{} {}".format(lot_num, total_cost))


def vehicle_exit(line):

    _data = line.split()

    try:
        num_plate = _data[1]
        timestamp = _data[2]
    except IndexError:
        print("Missing data detected. Please check file.")
        sys.exit()


    car_price = 2
    motorcycle_price = 1
    car_lot_detail, car_lot_timestamp = zip(*car_lot.values())
    motorcycle_lot_detail, motorcycle_lot_timestamp = zip(*motorcycle_lot.values())

    #if exiting vehicle is a car
    if num_plate in car_lot_detail:
        for lot_num, details in car_lot.items():
            #if exiting number plate matches a record in car lots
            if details[0] ==  num_plate:
                exit_timestamp = details[1]

                #free up lot
                car_lot[lot_num] = ["empty", "empty"]

                #calculate price
                try:
                    calculate_car_price(timestamp, exit_timestamp, car_price, lot_num)
                except ValueError:
                    print('Invalid timestamp detected. Please check file contents and try again.')
                break

    #if exiting vehicle is a motorcycle
    elif num_plate in motorcycle_lot_detail:
        for lot_num, details in motorcycle_lot.items():
            #if exiting number plate matches a record in motorcycle lots
            if details[0] ==  num_plate:
                exit_timestamp = details[1]

                #free up lot
                motorcycle_lot[lot_num] = ["empty", "empty"]

                #calculate price
                try:
                    calculate_motorcycle_price(timestamp, exit_timestamp, motorcycle_price, lot_num)
                except ValueError:
                    print('Invalid timestamp detected. Please check file contents and try again.')
                break
    else:
        #if exiting vehicle does not match any record
        print("Vehicle does not exist in carpark.")
        # break

def main(): 
    for i, line in enumerate(input_file):
        _data = line.split()
        if _data:
            action = _data[0]  
        else:
            continue

        if i != 0:
            if action == "Enter":
                vehicle_enter(line)
            elif action == "Exit":
                vehicle_exit(line)
            else:
                print("Invalid input record structure.")
                continue



if __name__ == '__main__':
    main()

