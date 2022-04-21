import pickle
import socket
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import threading
import time 

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import binascii



#initializations
kab = ''
N2 = 0 
KAlice = b"this is 24 byte Alice ke"
N1 = get_random_bytes(8)

def recv_Kb_msg():
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
        recv_msg2_from_bob = socket1.recv(1024) 
        print("\nprotocol message 4 Hex:\n", hex(int.from_bytes(recv_msg2_from_bob, 'big')), "\n" )
        recv_msg2_from_bob = pickle.loads(recv_msg2_from_bob)
        print("log: recieved reply from bob")
        print("log: verifing bob challenge")

        time.sleep(2)
        N2_1_N3 = get_N2_1_N3(recv_msg2_from_bob, kab)
        if N2_1_N3[0] == N2-1:
            print("log: bob is authorized, sending challenge reply.")
        N3_int = int.from_bytes(N2_1_N3[1], 'big')
        kab_N3_1 = get_Kab_N2(kab, N3_int-1)
        kab_N3_1 = pickle.dumps(kab_N3_1)
        socket1.send(kab_N3_1)

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
        print("the tickct is:", data[2], "and the size is:", len(data[3]))

        #set Kab and N2 as global variable so that thread 1 can 
        #use it to encrypt data to bob
        global kab 
        kab = data[2]
        Alice_private_key = ec.generate_private_key(ec.SECT163R2())
        Alice_public_key =  binascii.b2a_hex(Alice_private_key.public_key().public_numbers().encode_point()).decode()
        Kab_Ta_iv = encrypt_Ta(data[2], Alice_public_key)

        N1_int = int.from_bytes(N1, 'big')
        global N2
        N2 = N1_int - 1

        Kab_N2_iv = get_Kab_N2(data[2], N2)
        
        #below to verify that the communication is to bob
        if data[1] != "Bob":
            break
        data_to_bob = pickle.dumps([data[3], Kab_N2_iv])

        #send data to bob
        #recieved on thread 1
        socket1.send(data_to_bob)
        print("\nprotocol message 3 hex:\n", hex(int.from_bytes(data_to_bob, 'big')), '\n')
        print("log: sending chanllenge to bob")
        break

def get_Kab_N2(Kab, N2):
    cipher = DES3.new(Kab, DES3.MODE_CBC)
    data =  pickle.dumps([N2])
    i=0

    #below while loop for padding
    while True:
        i+=1
        if len(pickle.dumps([N2, 'a' * i ])) % 8 == 0:
            data = pickle.dumps([N2, 'a'* i ])
            break
        
    Kab_N2 = cipher.encrypt(data)
    return [Kab_N2, cipher.iv] 

def decrypt_data_from_KDC(msg):
    #msg[1] is the inilization function msg[0] are ecncrypted data
    cipher = DES3.new(KAlice, DES3.MODE_CBC, msg[1])
    data = cipher.decrypt(msg[0])
    data = pickle.loads(data)
    return data      

def get_N2_1_N3(msg, kab):
    cipher = DES3.new(kab, DES3.MODE_CBC, msg[1])
    N2_1_N3 = cipher.decrypt(msg[0])
    N2_1_N3 = pickle.loads(N2_1_N3)
    N2_1_N3 = pickle.loads(N2_1_N3[0])
    return N2_1_N3

def encrypt_Ta(Kab, Alice_public_key):
    cipher = DES3.new(Kab, DES3.MODE_CBC)
    
    Kab_Ta_Iv = cipher.encrypt(Alice_public_key)

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



