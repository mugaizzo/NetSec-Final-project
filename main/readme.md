# NetSec-Final-project
## SMS encryption
### This is the final project main folder
Unitl now the final idea is to use Needham-shroger with DH and authentication with 2FA and private keys.

 ![image](https://user-images.githubusercontent.com/15838537/165922951-1c608164-8915-40ac-a266-d9c922994a81.png)

  


## Major changes:
- Using CRC as the message size 160 byte is divisable by block size 64 bit.
- To minimize key size and maximize security we will use ECDH. so no need for smaller dh groups. 


## To run:
    - python bob.py
    - python OS_kdc.py
    - python Alice.py
