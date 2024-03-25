from __future__ import print_function
from PCANBasic import *
import random
import time
import os.path
import datetime
import sys


unused_bits = {'0422': [0, '24'], '022A': [0, '00'], '03B3': [0, '1F'], '02F9': [1, '00'], '034F': [1, 'FF'], '0232': [0, '00'], '02BF': [0, 'FF'], '0379': [2, '70'], '03BE': [0, 'FE'], '0096': [1, '00'], '03A7': [0, 'FF'], '0200': [3, '00'],
 '03B5': [0, 'FF'], '0330': [1, '4A'], '01E1': [2, '00'], '02A0': [2, 'F8'], '035E': [1, 'F0'], '0375': [0, '7F'], '0663': [0, 'F0'], '02E0': [0, 'FF'], '03A0': [0, 'FF'], '03BB': [0, '03'], '02FC': [1, '00'], '0202': [1, 'FF'], '01E4': [5, '11'],
 '03AC': [0, 'FE'], '02BB': [4, 'F2'], '0328': [3, '0F'], '01D6': [1, 'C0'], '0289': [0, 'FF'], '0423': [0, 'B8'], '05ED': [0, '6E'], '0351': [0, '15'], '0567': [0, '00'], '0366': [6, 'F0'], '02D5': [1, 'FF'], '0360': [0, '11'], '02D3': [0, '00'],
 '0199': [0, 'FF'], '0246': [1, 'F3'], '0130': [1, 'F0'], '0297': [2, 'F1'], '02A6': [0, '00'], '0304': [1, 'FF'], '024D': [1, 'FF'], '0231': [0, 'FC'], '03E6': [0, 'FF'], '02DF': [0, 'E1'], '030A': [1, 'FF'], '02C5': [5, '70'], '02C3': [1, '15'],
 '01BA': [0, 'FF'], '05E0': [2, '00'], '0349': [4, '00'], '05E7': [0, '99'], '0314': [2, 'FF'], '0661': [0, 'F0'], '01AE': [0, 'F7'], '0672': [0, 'F0'], '021A': [2, 'F7'], '02F8': [4, 'AF'], '00F3': [3, 'C0'], '019F': [0, 'FF'], '0393': [1, '32'],
 '02E6': [3, '32'], '0414': [2, '80'], '0510': [0, '00'], '0257': [2, 'FF'], '0435': [0, '00'], '026E': [1, '40'], '01A0': [7, 'FF'], '02E5': [2, '11'], '0667': [0, 'F0'], '019A': [0, 'FF'], '0572': [0, '00'], '00EC': [0, 'FF'], '01A5': [0, 'FF'],
 '02C4': [2, 'FF'], '02D9': [1, 'FF'], '02F7': [0, '0C'], '045C': [0, 'FF'], '0253': [1, '13'], '012F': [3, 'DD'], '0302': [0, 'FF'], '00A5': [7, 'F1'], '0656': [0, 'F0'], '02EB': [2, '12'], '0369': [0, 'FF'], '0301': [0, 'FF'], '05F2': [0, '6E'],
 '036A': [0, 'F5'], '02D6': [0, 'FF'], '0367': [2, '00'], '0242': [1, 'F3'], '01B9': [1, 'FF'], '03D3': [0, 'FF'], '0163': [0, 'FF'], '0678': [0, 'F0'], '0561': [0, '00'], '035C': [1, 'A0'], '02D2': [1, 'FF'], '019B': [2, '40'], '01B3': [0, 'FC'],
 '00F0': [0, 'F4'], '02F0': [1, 'DD'], '02CF': [0, 'F8'], '02EA': [0, 'FF'], '0226': [1, 'FF'], '0173': [2, '00'], '02D1': [0, 'FF'], '034B': [1, 'FF'], '0362': [1, '11'], '030B': [4, '30'], '03F9': [7, '6C'], '02F4': [0, '00'], '032E': [0, 'FF'],
 '05D6': [0, '6E'], '066D': [0, 'F0'], '0412': [3, '9B'], '040F': [0, '00'], '01EE': [1, 'FC']}


cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Label']

PCAN_CHANNELs = [PCAN_USBBUS1, PCAN_USBBUS2, PCAN_USBBUS3, PCAN_USBBUS4, PCAN_USBBUS5, PCAN_USBBUS6]

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Please dataset type: (e.g, Attack-Dos, Normal etc)")
        dataset_type = input("Please dataset type: ")
    else:
        dataset_type = sys.argv[1]
    
    x = datetime.datetime.now()
    x = "Dataset\\BMW " + dataset_type + " Dataset " + str(x).split()[0] + "-"
    ind = 0

    while os.path.isfile( x + str(ind) + ".txt"):
        ind += 1
        print("Yes")

    print("No")
    x = x + str(ind) + ".txt"
    f = open(x, "a")

    # all_data = "No\tID\tTYPE\tLEN\tONE\tTWO\tTHREE\tFOUR\tFIVE\tSIX\tSEVEN\tEIGHT\n"
    all_data = ""
    for col in cols:
        all_data += col + "\t"

    print(all_data)
    f.write(all_data + "\n")
    def update_progress(progress):  
        print("\r progress [{0}] {1}%".format('#'*(progress//10), progress), end='')
    

    CAN = PCANBasic()                            #CANi
    # if int(sys.argv[2]) >= 6 and int(sys.argv[2]) < 0:
    #     channel_input = input("Please channel number(0~5): ")
    #     CAN_BUS = PCAN_CHANNELs[int(channel_input)]
    # else:
    #     CAN_BUS = PCAN_CHANNELs[int(sys.argv[2])]
    CAN_BUS = PCAN_USBBUS1
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt

    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    print("Succesfully Connected")
    counter = 0
    start_time = time.time()
    ind = 1
    IsFirst = True
    while True: 
        mess = CAN.Read(CAN_BUS)    
        if mess[0] != PCAN_ERROR_QRCVEMPTY:
            label_data = "Legitimate"
            all_data = str(ind) + ')' + "\t"

            if IsFirst:
                offset = 0
                start_time = mess[2].micros + 1000 * mess[2].millis + 0x100000000 * 1000 * mess[2].millis_overflow
                start_time = start_time / 1000
                # start_time = readResult[2].millis
                IsFirst = False
            else:
                current_time = mess[2].micros + 1000 * mess[2].millis + 0x100000000 * 1000 * mess[2].millis_overflow
                # current_time = readResult[2].millis
                current_time = current_time / 1000
                offset = (current_time - start_time)
            
            all_data += "{:.3f}".format(offset) + "\t"
            
            id_hex = hex(mess[1].ID)[2:]
            for _ in range(4 - len(id_hex)):
                id_hex = '0' + id_hex.upper()
            
            all_data += str(mess[1].MSGTYPE) + "\t" + id_hex + "\t" + str(hex(mess[1].LEN)[2:]) 

            for j in range(mess[1].LEN):
                if id_hex in unused_bits:
                    check_val = int(unused_bits[id_hex][1], 16)
                    check_ind = int(unused_bits[id_hex][0])

                    if check_ind == j and mess[1].DATA[check_ind] == (check_val + 1):
                        print("Replay")
                        label_data = "Replay"
                        data_hex = hex(mess[1].DATA[j] - 1)[2:]
                    elif check_ind == j and mess[1].DATA[check_ind] == ( check_val + 2):
                        print("DoS")
                        label_data = "DoS"
                        data_hex = hex(mess[1].DATA[j] - 2)[2:]
                    elif check_ind == j and mess[1].DATA[check_ind] == ( check_val + 3):
                        print("Fuzzy")
                        label_data = "Fuzzy"
                        data_hex = hex(random.randrange(0, 255))[2:]
                    else:
                        data_hex = hex(mess[1].DATA[j])[2:]  
                else:
                    data_hex = hex(mess[1].DATA[j])[2:]  

                for _ in range(2 - len(data_hex)):
                    data_hex = '0' + data_hex.upper()

                all_data += "\t" + data_hex.upper()
            for _ in range(mess[1].LEN, 8):
                all_data += "\t" + "-1"
                
            all_data += "\t" + label_data 
            all_data += "\n"
            ind += 1
            print(all_data)
            f.write(all_data)

    # All initialized channels are released
    CAN.Uninitialize(PCAN_NONEBUS)
