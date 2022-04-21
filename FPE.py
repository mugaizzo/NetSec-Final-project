from Crypto.Cipher import AES
from base64 import b64encode

key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_EAX)

ciphertext, tag = cipher.encrypt_and_digest(b'helloo')
nonce = cipher.nonce


print(tag)
print(ciphertext)
print(len(b'helloo'))
################################################
key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_CFB)

ct_bytes = cipher.encrypt(b'helloo')
iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')

print(ct_bytes)
print(iv)
print(ct)
print(len(ct_bytes))