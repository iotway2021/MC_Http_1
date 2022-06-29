import configparser 
from src.pymcprotocol import Type3E
from src.pymcprotocol import Type4E
 
import json  
import threading
import time
import requests                                                                         
from datetime import datetime
import sys
publishInterval=5
url = 'https://emslte.arkaautomaations.com/teltonika_test.php'  
ini = configparser.ConfigParser()
ini.read('./config.ini')
#pyinstaller.exe --onefile .\MC_MQTT.py 
publishDic ={}

def get_config(settings):
    #pytest execute this file in parent directory
    
    plctype = ini[settings]["PLC"]
    ip = ini[settings]["ip"]
    port = ini[settings].getint("port")
    addr = ini[settings]["address"]
     
    return plctype, ip, port,addr 

def Initialize_pymcprotocol(type,plctype, ip, port,arrd):
     
    if type=="3E":
        pyplc = Type3E(plctype)
    else:
        pyplc = Type4E(plctype)
     
    while(pyplc._is_connected == False):
        
        try:
            print("trying to connect with ip:port "+str(ip)+':'+str(port))
            pyplc.connect(ip, port)
            print("connected "+str(datetime.now()))
        except:
            print("Failed to connect the PLC "+str(datetime.now()))
            time.sleep(5)
      
    dicdata={}         
    while True:
        for address in arrd:
            adres_array=str(address).split(':')
            plcTag_address=adres_array[0]
            plcTag_datatype=adres_array[1]
            plcTag_length=adres_array[2]
            if plcTag_datatype=='integer':
                value = pyplc.batchread_wordunits(plcTag_address, 1)
                print(plcTag_address+" "+str(value[0]))
                dicdata[plcTag_address]= value[0]
            elif plcTag_datatype=='string':
                string_value = pyplc.batchread_string(plcTag_address, plcTag_length)
                print(plcTag_address+" "+str(string_value[0]))
                dicdata[plcTag_address]= string_value[0]
             
            
        dicdata["ts"]= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        json_object = json.dumps(dicdata)
        print(json_object)
        x = requests.post(url, data = json_object) 
        time.sleep(publishInterval)
    #value = pyplc.batchread_bitunits("M10", 3)
       
    #word_values, dword_values = pyplc.randomread(["D2000", "D2010", "D2020"], ["D2040", "D2050", "D2060", "D2070", "D2080"])

 

if __name__ == "__main__":
    plctype1,ip1, port1,addr1 =get_config('PLC1settings') 
    plc1 = threading.Thread(target=Initialize_pymcprotocol, args=("3E",plctype1, ip1, port1,addr1))
    plc1.start() 
    plctype2, ip2, port2,addr2 =get_config('PLC2settings') 
    plc2 = threading.Thread(target=Initialize_pymcprotocol, args=("3E",plctype2, ip2, port2, addr2))
    plc2.start() 
    plctype3, ip3, port3,addr3 =get_config('PLC3settings') 
    plc3 = threading.Thread(target=Initialize_pymcprotocol, args=("3E",plctype3, ip3, port3, addr3))
    plc3.start() 
    plctype4, ip4, port4,addr4 =get_config('PLC4settings') 
    plc4 = threading.Thread(target=Initialize_pymcprotocol, args=("3E",plctype4, ip4, port4,addr4))
    plc4.start() 
     
    
