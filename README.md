# NetSec-Final-project
## SMS encryption
### This is the final project main folder
Unitl now the final idea is to use Needham-shroger with DH and authentication with 2FA and private keys.

  
  
![11fig18](https://user-images.githubusercontent.com/15838537/164345281-5a141529-3b0a-4973-9217-efa8b90f0f37.jpg)

# Major changes:
- Using CRC as the message size 160 byte is divisable by block size 64 bit.
- To minimize key size and maximize security we will use ECDH. so no need for smaller dh groups. 
