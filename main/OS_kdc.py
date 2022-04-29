from copyreg import pickle
import socket
import pickle
from wsgiref.util import request_uri
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import time
import threading


def generate_ticket(Kab):
    cipher = DES3.new(Kbob, DES3.MODE_CBC)
    data = cipher.encrypt(Kab)
    ticket_iv = cipher.iv+data
    return ticket_iv

def encrypt_ticket(K_kdc,ticket_iv):
    cipher = DES3.new(K_kdc, DES3.MODE_CBC)
    K_kdc_ticket = cipher.encrypt(ticket_iv)
    return (K_kdc_ticket , cipher.IV)

def decrypt_ticket_frm_bob(K_kdc, K_kdc_ticket_frm_bob, K_kdc_iv ):
    cipher = DES3.new(K_kdc, DES3.MODE_CBC, K_kdc_iv)
    ticket_frm_bob = cipher.decrypt(K_kdc_ticket_frm_bob)
    return ticket_frm_bob 

def alice_verification():
    socket_alice_2fa = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_alice_2fa.connect(("127.0.0.1", 55566))
    alice_random = get_random_bytes(6)
    socket_alice_2fa.send(alice_random)
    random_from_alice = socket_alice_2fa.recv(1024)
    if random_from_alice == alice_random:
        print("log: Alice verified!")
        exit()

def bob_verification():
    socket2fa = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket2fa.bind(('localhost', 44477))
    socket2fa.listen(10)
    connection1, addr = socket2fa.accept()
    bob_request = connection1.recv(1024)
    if bob_request[:21] == b'recived this from bob':
        print('log: message from bob')
        print("log: Verifing Bob with 2FA")
        bob_random = get_random_bytes(6)
        connection1.send(bob_random)
        random_from_bob = connection1.recv(1024)
        if random_from_bob == bob_random:
            K_kdc_ticket_frm_bob = bob_request[21:]
            ticket_iv_frm_bob = decrypt_ticket_frm_bob(K_kdc, K_kdc_ticket_frm_bob, K_kdc_iv )
            if ticket_iv_frm_bob == ticket_iv:
                print("log: Bob verified!")
                print("log: sending ticket!")
                connection1.send(ticket_iv)



#bob and alice keys
Kbob = b" this is 24 byte bob key"
KAlice = b"this is 24 byte Alice ke"
K_kdc = b" this is 24 byte kdc key"

#main logic starts here
print("\n\n\nHI I'M THE KDC", "\nWaiting for requests.")
print("\nlog: listening  on localhost:5555\n")


while True:
    #opening socket
    socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket1.bind(('localhost', 5555))
    socket1.listen(10)
    connection1, addr = socket1.accept()
    #recieve message 
    msg = connection1.recv(1024)
    msg = pickle.loads(msg)
    time.sleep(1)
    print("log: recieved something...")
    #if message contain Alice wants Bob reply back with needed ticket
    if msg[0] == "Alice wants Bob":
        print("log: Alice wants Bob")
        print("log: Verifing Alice with 2FA")
        t1 = threading.Thread(target=alice_verification)
        t1.start()
        t1.join()
        #generating ticket
        time.sleep(1)
        Kab = get_random_bytes(24)
        ticket_iv = generate_ticket(Kab)
        
        #encrypting ticket with K_kdc
        K_kdc_ticket, K_kdc_iv = encrypt_ticket(K_kdc,ticket_iv)

        #encrypting message
        cipher = DES3.new(KAlice, DES3.MODE_CBC)
        data = pickle.dumps(["Bob", Kab, K_kdc_ticket, "pading   "])
        reply = cipher.encrypt(data)
        #reply to Alice
        connection1.send(pickle.dumps([reply, cipher.iv]))
        print("log: replied to Alice")
        print("log: waiting for Bob contact")
        t_bob = threading.Thread(target=bob_verification)
        t_bob.start()
        t_bob.join()
        print("------------------------------------")  
    socket1.close()

    

