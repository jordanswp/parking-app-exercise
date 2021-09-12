# Zendesk Parking App Exercise

## A command line parking system app written with Python.

## Requirements:
- Python 3.8.4

## Running the app:

Run the file via command line and upload file when prompted:
1. Valid file: ./upload_file/valid_input/valid_input.txt
2. Invalid files: ./upload_file/invalid_input/{select file}

```
python3 parking-app.py
```

Input:
```
3 4 
Enter motorcycle SGX1234A 1613541902 
Enter car SGF9283P 1613541902 
Exit SGX1234A 1613545602 
Enter car SGP2937F 1613546029 
Enter car SDW2111W 1613549730 
Enter car SSD9281L 1613549740 
Exit SDW2111W 1613559745  
```

The first line of input creates a car park dictionary of 7 total available lots; 3 car lots and 4 motorcycle lots.

```
car_park = {
    "car_lot": {
        "CarLot1": ["empty", "empty"],
        "CarLot2": ["empty", "empty"],
        "CarLot3": ["empty", "empty"],
    },
    "motorcycle_lot": {
        "MotorcycleLot1": ["empty", "empty"],
        "MotorcycleLot2": ["empty", "empty"],
        "MotorcycleLot3": ["empty", "empty"],
    }
}
```

The first index of the ["empty", "empty"] array signifies the vehicle plate number while the second index stores the timestamp.

Upon a vehicle entering the parking lot, the parking lot with the lowest index will be filled first.
```
Enter motorcycle SGX1234A 1613541902 
```
```
car_park = {
    "car_lot": {
        "CarLot1": ["empty", "empty"],
        "CarLot2": ["empty", "empty"],
        "CarLot3": ["empty", "empty"],
    },
    "motorcycle_lot": {
        "MotorcycleLot1": ["SGX1234A", "1613541902"],
        "MotorcycleLot2": ["empty", "empty"],
        "MotorcycleLot3": ["empty", "empty"],
    }
}
```

And upon a vehicle leaving, the respective lot will be vacated and the parking fee would be calculated.

When a particular parking lot is full, vehicles would be rejected from entering the car park. 

```
Output:
Accept MotorcycleLot1
Accept CarLot1
MotorcycleLot1 2
Accept CarLot2
Accept CarLot3
Reject
CarLot3 6
```