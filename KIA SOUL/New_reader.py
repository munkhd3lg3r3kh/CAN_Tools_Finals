from __future__ import print_function
from PCANBasic import *
import os.path
import datetime
import sys
import keyboard
from ctypes import *

cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']
    
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Please dataset type: (e.g, Attack-Dos, Normal etc)")
        dataset_type = input("Please dataset type: ")
    else:
        dataset_type = sys.argv[1]
    
    x = datetime.datetime.now()
    x = "Dataset\\KIA " + dataset_type + " Dataset " + str(x).split()[0] + "-"
    ind = 0

    while os.path.isfile( x + str(ind) + ".txt"):
        ind += 1
        print("Yes")

    print("No")
    x = x + str(ind) + ".txt"
    f = open(x, "a")
    all_data = ""
    for col in cols:
        all_data += col + "\t"

    print(all_data)
    f.write(all_data + "\n")
    def update_progress(progress):
        print("\r progress [{0}] {1}%".format('#'*(progress//10), progress), end='')
    

    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS6
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    start_time = 0
    readResult = PCAN_ERROR_OK,
    IsFirst = True
    ind = 1
    while True:
        # Check the receive queue for new messages
        #
        readResult = CAN.Read(CAN_BUS)
        if readResult[0] != PCAN_ERROR_QRCVEMPTY:
            # Process the received message
            #
            print("A message was received")
            all_data = str(ind) + ')' + "\t"
            if IsFirst:
                offset = 0
                start_time = readResult[2].micros + 1000 * readResult[2].millis + 0x100000000 * 1000 * readResult[2].millis_overflow
                start_time = start_time / 1000
                # start_time = readResult[2].millis
                IsFirst = False
            else:
                current_time = readResult[2].micros + 1000 * readResult[2].millis + 0x100000000 * 1000 * readResult[2].millis_overflow
                # current_time = readResult[2].millis
                current_time = current_time / 1000
                offset = (current_time - start_time)
            
        
            all_data += "{:.3f}".format(offset) + "\t"
            id_hex = hex(readResult[1].ID)[2:]
            for _ in range(4 - len(id_hex)):
                id_hex = '0' + id_hex.upper()
            
            all_data += str(readResult[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(readResult[1].LEN)[2:]) 
                
            for j in range(readResult[1].LEN):
                data_hex = hex(readResult[1].DATA[j])[2:]  
                for _ in range(2 - len(data_hex)):
                    data_hex = '0' + data_hex.upper()
                all_data += "\t" + data_hex.upper()

            for _ in range(readResult[1].LEN, 8):
                all_data += "\t" + "-1"
                
            all_data += "\t" 
            all_data += "\n"
            ind += 1
            print(all_data)
            f.write(all_data)
            if keyboard.is_pressed('k'):
                break
    CAN.Uninitialize(PCAN_NONEBUS)