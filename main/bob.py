
from copyreg import pickle
import socket
from tkinter import N
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import pickle
import time

#bob key
Kbob = b" this is 24 byte bob key"

def generateKbob_Nb():
    cipher = DES3.new(Kbob, DES3.MODE_CBC)
    Nbob = get_random_bytes(8)
    Kbob_Nb_Iv = [cipher.iv, cipher.encrypt(Nbob)]
    return Kbob_Nb_Iv
    
def get_Kab(ticket_iv):
    cipher = DES3.new(Kbob, DES3.MODE_CBC, ticket_iv[1])
    ticket = cipher.decrypt(ticket_iv[0])
    ticket = pickle.loads(ticket)
    return ticket[0]

def get_N2(Kab, Kab_N2_iv):
    cipher = DES3.new(Kab, DES3.MODE_CBC, Kab_N2_iv[1])
    ticket = cipher.decrypt(Kab_N2_iv[0])
    ticket = pickle.loads(ticket)
    return ticket[0]

def get_Kab_N2_1_N3_iv(Kab, N2, N3):
    cipher = DES3.new(Kab, DES3.MODE_CBC)
    N2_1_N3 = pickle.dumps([N2-1, N3])
    i=0
    while True:
        i+=1
        if len(pickle.dumps([N2_1_N3, 'a'* i ])) % 8 == 0:
            N2_1_N3 = pickle.dumps([N2_1_N3, 'a'* i ])
            break


    Kab_N2_1_N3 = cipher.encrypt(N2_1_N3)
    Kab_N2_1_N3_iv = pickle.dumps([Kab_N2_1_N3, cipher.iv])
    return Kab_N2_1_N3_iv

def get_N3_1(msg3, Kab):
    cipher = DES3.new(Kab, DES3.MODE_CBC, msg3[1])
    ticket = cipher.decrypt(msg3[0])
    ticket = pickle.loads(ticket)
    return ticket[0]


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
    msg2 = pickle.loads(msg2)
    #decrypting and getting Kab
    Kab = get_Kab(msg2[0])
    #using kab to get N2
    N2 = get_N2(Kab, msg2[1])
    #generating N2
    N3 = get_random_bytes(8)
    N3_int = int.from_bytes(N3, 'big')
    Kab_N2_1_N3_iv = get_Kab_N2_1_N3_iv(Kab, N2, N3)
    #sending reply to Alice
    connection1.send(Kab_N2_1_N3_iv)
    print("log: sending challenge to Alice")
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

