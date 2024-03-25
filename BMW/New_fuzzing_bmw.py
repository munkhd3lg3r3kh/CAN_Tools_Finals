from PCANBasic import *
import time
import random
import datetime
import os


used_ids = []

with open("Used_ids/bmw_used_ids.txt", 'r') as file:
        for line in file:
            used_ids.append(line.strip())




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

# x = datetime.datetime.now()
# x = "Dataset\\Fuzzing Attack Injected Datas " + str(x).split()[0] + "-"
# ind = 0

# while os.path.isfile( x + str(ind) + ".txt"):
#     ind += 1
#     print("Yes")

# print("No")
# x = x + str(ind) + ".txt"
# f = open(x, "a")




def Fuzzing_Attack(id, leng, data):
    all_datas = ""
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(id, 16)
    Fuzzing_attack.LEN = leng
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.LEN) + "\t"

    for i in range(leng):
        Fuzzing_attack.DATA[i] = data[i]
        all_datas += str(data[i]) + "\t"

    # CAN.Write(CAN_BUS, Fuzzing_attack)
    print(all_datas)
    all_datas += "\n"
    # f.write(all_datas)

if __name__ == "__main__":
    # CAN = PCANBasic()                            #CANi
    # CAN_BUS = PCAN_USBBUS1
    # counter = 0    
    # start_time = time.time()
    # ind = 0
    # result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    # id_exist = False
    # if result != PCAN_ERROR_OK:
    #     # An error occurred, get a text describing the error and show it
    #     #
    #     print("oh No")
    #     CAN.GetErrorText(result)
    #     print(result)
    inde = 0
    while inde < 10:
        time_offset = 0.05
        
        injection_id = '{:04x}'.format(random.randint(0, 1024)).upper()

        while injection_id in used_ids:
            injection_id = '{:04x}'.format(random.randint(0, 1024)).upper()
        
                        
        print(bcolors.OKBLUE + str(injection_id) + bcolors.ENDC)
        attack_data = []

        leng = random.randint(2, 8)

        for _ in range(leng):
            attack_data.append(random.randint(0, 255))

        Fuzzing_Attack(injection_id, leng, attack_data)
        time.sleep(time_offset)
        inde += 1