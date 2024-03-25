from __future__ import print_function
from PCANBasic import *
import time
import keyboard
import datetime
import sys
import os


cols = ["Label", "No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Label']
    

time_range = {'0165': [8.6, 11.4], '02B0': [7.5, 12.6], '04B0': [17.8, 22.2], '0164': [7.4, 13.0], '0370': [7.5, 12.5], '043F': [7.2, 12.7],
 '0440': [6.7, 13.3], '0316': [6.8, 13.2], '018F': [7.8, 12.1], '0080': [8.0, 11.5], '0081': [8.0, 11.5], '0260': [7.2, 12.7],
 '02A0': [7.2, 12.7], '0153': [8.9, 11.3], '0220': [7.9, 12.1], '0329': [6.9, 12.8], '0382': [17.7, 22.3], '0545': [6.2, 13.7],
 '04F0': [16.8, 23.2], '04B1': [17.6, 22.7], '0350': [16.6, 23.5], '01F1': [18.1, 21.9], '02C0': [97.2, 102.1], '04F2': [16.7, 23.3],
 '0120': [199.1, 200.8], '0587': [96.0, 104.1], '0510': [96.9, 103.1], '05E4': [96.2, 103.9], '059B': [97.8, 102.2], '0110': [99.0, 101.1],
 '04F1': [98.5, 101.5], '0690': [95.7, 104.0], '05F0': [196.0, 203.5], '0034': [999.3, 1000.8], '05A0': [994.9, 1001.8], '05A2': [995.3, 1001.8],
 '0042': [999.4, 1000.1], '0043': [999.4, 1000.1], "0410": [195, 205]}

time_offs = {}

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

    # all_data = "No\tID\tTYPE\tLEN\tONE\tTWO\tTHREE\tFOUR\tFIVE\tSIX\tSEVEN\tEIGHT\n"
    all_data = ""
    for col in cols:
        all_data += col + "\t"

    print(all_data)
    f.write(all_data + "\n")
    def update_progress(progress):
        print("\r progress [{0}] {1}%".format('#'*(progress//10), progress), end='')
    

    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS1
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt

    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    counter = 0
    start_time = time.time()
    ind = 1
    IsFirst = True
    
    while True:
        # Check the receive queue for new messages
        #
        mess = CAN.Read(CAN_BUS)
        if mess[0] != PCAN_ERROR_QRCVEMPTY:
            # Process the received message
            #
            
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

            id_hex = hex(mess[1].ID)[2:].upper()
            for _ in range(4 - len(id_hex)):
                id_hex = '0' + id_hex

            if id_hex in time_range:
                if id_hex in time_offs:
                    spec_offset = time_offs[id_hex]
                    last_offset = spec_offset[len(spec_offset)-1]
                    
                    min_off = time_range[id_hex][0]
                    max_off = time_range[id_hex][1]
                    diff = offset - last_offset
                    
                    if diff >= min_off and diff <= max_off:
                        label = "[Normal]"
                    else:
                        label = "[Attack]"
							
                    time_offs[id_hex].append(offset)
                    if len(time_offs[id_hex]) > 100:
                        time_offs[id_hex].pop(0)
                        time_offs[id_hex].pop(0)
                
                else:
                    time_offs[id_hex] = [offset]
                    diff = 0
                    label = "[Normal]"
            else:
                diff = 0
                label = "[Normal]"
            all_datas = label + "\t"
            all_datas += str(ind) + ')' + "\t"
            ind += 1
            all_datas += "{:.3f}".format(offset) + "\t"
            all_datas += str(id_hex) + "\t"
            all_datas += str(diff) + "\t" + str(hex(mess[1].LEN)[2:])

            for j in range(mess[1].LEN):
                data_hex = hex(mess[1].DATA[j])[2:]  
                for _ in range(2 - len(data_hex)):
                    data_hex = '0' + data_hex.upper()
                all_datas += "\t" + data_hex.upper()
            
            for _ in range(mess[1].LEN, 8):
                all_datas += "\t" + "-1"
            
            print(all_datas)
            all_datas += "\n"
            f.write(all_datas)
        if keyboard.is_pressed('k'):
            break
    CAN.Uninitialize(PCAN_USBBUS6)