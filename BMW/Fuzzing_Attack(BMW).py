from PCANBasic import *
import time
import random
import datetime
import os


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




def Fuzzing_Attack(id, leng, data):
    all_datas = ""
    Fuzzing_attack = TPCANMsg()
    Fuzzing_attack.ID = int(id, 16)
    Fuzzing_attack.LEN = leng
    Fuzzing_attack.MSGTYPE = PCAN_MESSAGE_STANDARD
    all_datas += str(hex(Fuzzing_attack.ID)) + "\t" + str(Fuzzing_attack.LEN)

    if id in unused_bits:
        check_ind = unused_bits[id][0]
        check_val = unused_bits[id][1]
    else:
        check_ind = 123
        check_val = 123
    
    for i in range(leng):
        if check_ind == i and check_val == data[i]:            
            Fuzzing_attack.DATA[i] = int(data[i], 16) + 3
            all_datas += "\t" + bcolors.OKGREEN + str(hex(Fuzzing_attack.DATA[i])) + bcolors.ENDC
        else:
            Fuzzing_attack.DATA[i] = int(data[i], 16)
            all_datas += "\t" + str(hex(Fuzzing_attack.DATA[i]))
    
    CAN.Write(CAN_BUS, Fuzzing_attack)
    print(all_datas)
    all_datas += "\n"
    f.write(all_datas)

if __name__ == "__main__":
    CAN = PCANBasic()                            #CANi
    CAN_BUS = PCAN_USBBUS2
    counter = 0    
    start_time = time.time()
    ind = 0
    result = CAN.Initialize(CAN_BUS, PCAN_BAUD_500K, 2047, 0, 0) #Channel, Btr, HwType, IOPort, INterrupt
    id_exist = False
    if result != PCAN_ERROR_OK:
        # An error occurred, get a text describing the error and show it
        #
        print("oh No")
        CAN.GetErrorText(result)
        print(result)
    while True:
        # time_offset = random.randrange(1, 50) / 1000
        time_offset = 0.05
        
        injection_id = random.choice(list(unused_bits.keys()))
                        
        print(bcolors.OKBLUE + str(injection_id) + bcolors.ENDC)
        attack_data = []

        if injection_id in unused_bits:
            leng = 8
            id_exist = True
        else:
            leng = random.randrange(2, 8)
        
        for i in range(leng):
            if id_exist and i == unused_bits[injection_id][0]:
                attack_data.append(unused_bits[injection_id][1])
            else:
                attack_data.append(hex(random.randrange(0, 255)))
        id_exist = False
        Fuzzing_Attack(injection_id, leng, attack_data)
        time.sleep(time_offset)