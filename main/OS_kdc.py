from copyreg import pickle
import socket
import pickle
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import time

def generate_ticket(Kab):
    cipher = DES3.new(Kbob, DES3.MODE_CBC)
    data = cipher.encrypt(Kab)
    ticket_iv = cipher.iv+data
    return ticket_iv
    
#bob and alice keys
Kbob = b" this is 24 byte bob key"
KAlice = b"this is 24 byte Alice ke"

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
    if msg[1] == "Alice wants Bob":
        print("Alice wants Bob")
        #generating ticket
        time.sleep(1)
        Kab = get_random_bytes(24)
        ticket_iv = generate_ticket(Kab)
        print("heheh", len(ticket_iv))
        N1 = msg[0]
        #encrypting message
        cipher = DES3.new(KAlice, DES3.MODE_CBC)
        data = pickle.dumps([N1, "Bob", Kab, ticket_iv, "pading"])
        print("datadatelen", len(data))
        reply = cipher.encrypt(data)
        #reply to Alice
        connection1.send(pickle.dumps([reply, cipher.iv]))
        print("log: replied to Alice")
        print("------------------------------------")  
    socket1.close()

    

