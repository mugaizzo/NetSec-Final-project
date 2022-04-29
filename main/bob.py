
from copyreg import pickle
import imp
import socket
from tkinter import N
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import pickle
import time
from expo import expo


#bob key
Kbob = b" this is 24 byte bob key"


def get_Ta( Kab,Kab_Ta_Iv):
    cipher = DES3.new(Kab, DES3.MODE_CBC, Kab_Ta_Iv[0:8])
    Ta = cipher.decrypt(Kab_Ta_Iv[8:])
    return Ta

    
def get_Kab(ticket_iv):
    cipher = DES3.new(Kbob, DES3.MODE_CBC, ticket_iv[0:8])
    ticket = cipher.decrypt(ticket_iv[8:])
    return ticket


def encrypt_Tb(Kab, Tb):
    cipher = DES3.new(Kab, DES3.MODE_CBC)
    Kab_Tb = cipher.encrypt(Tb)
    return  cipher.IV + Kab_Tb

# main logic starts here
# Open socket and log initial messages
socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("\n\n\nHI I'M BOB")
socket1.bind(('localhost', 11223))
print("\nlog: listening  on localhost:11223\n")
socket1.listen(10)
print('log: waiting for connections.\n')    


msg = "NUL" 
while True:
    #accept new connections
    connection1, addr = socket1.accept()
    print("-----------------------------")
    print("connected to address", addr)
    #recieve message from bob
    msg2 = connection1.recv(1024)
    print("log: recieved message from Alice")
    time.sleep(1)

    if msg2[0:7] != b'ENC_MSG':
        print("log: normal message!\n")
        print("log: content is\n\n")
        print(msg)
        break

    ticket = msg2[7:39]
    Kab_Ta_Iv = msg2[39:]
    print("Kab_Ta_Iv \n\n", Kab_Ta_Iv)

    #decrypting and getting Kab
    Kab = get_Kab(ticket)
    #using kab to get Ta
    Ta = get_Ta(Kab ,Kab_Ta_Iv)
    Ta = int.from_bytes(Ta, 'big')
    

    Tb = expo(1907,12077,784313)
    Kab_Tb_iv = encrypt_Tb(Kab, Tb.to_bytes(8, 'big'))
    key= expo(Ta,12077,784313)
    print("key\n\n", key)
    

    #sending reply to Alice
    connection1.send(Kab_Tb_iv)
    print("log: sending challenge to Alice")
    print("Kab_Tb_iv\n\n", Kab_Tb_iv)

    time.sleep(1)
    msg3 = connection1.recv(1024)
    print("log: recieved reply from Alice")
    time.sleep(3)
    print("\nprotocol message 5:\n", hex(int.from_bytes(msg3, 'big')), "\n")
    msg3 = pickle.loads(msg3)
    N3_1 =  get_N3_1(msg3, Kab)
    if N3_1 == N3_int - 1:
        print("log: Alice is authenticated")

    break

