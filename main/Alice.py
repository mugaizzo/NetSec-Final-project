import pickle
import socket
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import threading
import time 

from expo import expo



#initializations
kab = ''
N2 = 0 
KAlice = b"this is 24 byte Alice ke"
N1 = get_random_bytes(8)

def recv_Kb_msg():
        global kab 
        #prepare message to kdc and serialize it to bytes
        msg3 = pickle.dumps([N1 ,"Alice wants Bob"])

        #open socket to KDC and send message
        kdc_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        kdc_socket.connect(("127.0.0.1", 5555))
        kdc_socket.send(msg3)
        print("log: sending to KDC\n")
        time.sleep(1)
        #open new thread to recieve message form KDC 
        #continue on fuction recv_Kb_msg()
        t2 = threading.Thread(target=recv_kdc_msg(kdc_socket))
        t2.start()

        #the ticket and Kab(N2) are sent inside recv_kdc_msg(kdc_socket)
        Kab_Tb_iv = socket1.recv(1024) 
        # print("\nprotocol message 4 Hex:\n", hex(int.from_bytes(Kab_Tb_iv, 'big')), "\n" )
        print("log: recieved reply from bob")
        print("log: verifing bob challenge")
        print("Kab_Tb_iv\n\n", Kab_Tb_iv)
        
        Tb = get_Tb(kab ,Kab_Tb_iv)
        Tb = int.from_bytes(Tb, 'big')
        
        key= expo(Tb,160031,784313)
        print("key\n\n", key)

        time.sleep(2)

        
        message_IV = encrypt_main_message(key.to_bytes(24, 'big'), 'hi this is the main message')
        socket1.send(message_IV)

def recv_kdc_msg(kdc_socket):
    while True:
        #recieve message form KDC
        msg = kdc_socket.recv(1024)
        print("log: recieved something from KDC")
        time.sleep(1)
        #deserialize it
        msg = pickle.loads(msg)

        #decrypt data form KDC using KAlice via below function
        data = decrypt_data_from_KDC(msg)
        print("the tickct is:", data[3], "and the size is:", len(data[3]))

        #set Kab and N2 as global variable so that thread 1 can 
        #use it to encrypt data to bob
        global kab 
        kab = data[2]
        Ta =  expo(1907,160031,784313)
        
        Kab_Ta_iv = encrypt_Ta(data[2], Ta.to_bytes(8, 'big'))
        print('Ta is\n\n', Ta)
        print('Kab_Ta_iv is\n\n', Kab_Ta_iv)


        
        #first DH message:
        data_to_bob = b'ENC_MSG' + data[3] + Kab_Ta_iv
        #send data to bob
        #recieved on thread 1
        socket1.send(data_to_bob)
        print("log: sending chanllenge to bob")
        break


def decrypt_data_from_KDC(msg):
    #msg[1] is the inilization function msg[0] are ecncrypted data
    cipher = DES3.new(KAlice, DES3.MODE_CBC, msg[1])
    data = cipher.decrypt(msg[0])
    data = pickle.loads(data)
    return data      

def encrypt_Ta(Kab, Ta):
    cipher = DES3.new(Kab, DES3.MODE_CBC)
    Kab_Ta = cipher.encrypt(Ta)
    return  cipher.IV + Kab_Ta

def get_Tb( Kab,Kab_Tb_Iv):
    cipher = DES3.new(Kab, DES3.MODE_CBC, Kab_Tb_Iv[0:8])
    Tb = cipher.decrypt(Kab_Tb_Iv[8:])
    return Tb

def encrypt_main_message(key, main_message):
    cipher = DES3.new(key, DES3.MODE_CBC)
    

#main logic start here
#open socket and pring initial messages
socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("\n\n\nHI I'M ALICE") 
#connect to bob and send "I want to talk to you"
socket1.connect(("127.0.0.1", 11223))
  
#open new thread to recieve message from bob
#continue on fuction recv_Kb_msg()
t = threading.Thread(target=recv_Kb_msg)
t.start()     



