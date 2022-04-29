

import socket
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import threading
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

def get_main_message(key, main_message_enc, main_msg_iv):
    cipher = DES3.new(key, DES3.MODE_CBC, main_msg_iv)
    main_message = cipher.decrypt(main_message_enc)
    return main_message


def encrypt_Tb(Kab, mainIV_Tb):
    cipher = DES3.new(Kab, DES3.MODE_CBC)
    Kab_mainIV_Tb = cipher.encrypt(mainIV_Tb)
    return  cipher.IV + Kab_mainIV_Tb


def Bob_2FA():
    global ticket
    socket_bob_2fa = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_bob_2fa.connect(("127.0.0.1", 44477))
    socket_bob_2fa.send(b'recived this from bob'+ticket)
    twoFactrandom = socket_bob_2fa.recv(1024) 
    socket_bob_2fa.send(twoFactrandom)
    ticket = socket_bob_2fa.recv(1024)


    
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
    print("log: encrypted message! fetching KDC address and verifing")
    global ticket
    ticket = msg2[7:39]

    thread_2fa = threading.Thread(target=Bob_2FA) 
    thread_2fa.start()
    thread_2fa.join()
    
    g = msg2[39:61]
    p = msg2[61:69]
    Kab_Ta_Iv = msg2[69:]
    

    #decrypting and getting Kab
    Kab = get_Kab(ticket)
    #using kab to get Ta
    Ta = get_Ta(Kab ,Kab_Ta_Iv)
    Ta = int.from_bytes(Ta, 'big')
    

    Tb = expo(45456456,120212177,1342342345234391432678)
    main_msg_iv = get_random_bytes(8)
    Kab_mainIV_Tb_iv = encrypt_Tb(Kab, main_msg_iv+Tb.to_bytes(16, 'big'))
    key= expo(Ta,120212177,1342342345234391432678)
    
    

    #sending reply to Alice
    connection1.send(Kab_mainIV_Tb_iv)
    print("log: sending challenge to Alice")
    

    time.sleep(1)
    main_message_enc = connection1.recv(1024)
    print("log: recieved main message from Alice")
    time.sleep(3)
    
    main_message =  get_main_message(key.to_bytes(24, 'big'), main_message_enc,main_msg_iv)
    print("recived message:\n", str(main_message, 'utf-8') )

    break

