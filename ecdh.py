from Crypto.Random import get_random_bytes



from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import binascii


Bob_private_key = ec.generate_private_key(ec.SECT163R2())
Bob_public_key = binascii.b2a_hex(Bob_private_key.public_key().public_numbers().encode_point()).decode()

print(Bob_public_key)
print(len(Bob_public_key))

Alice_private_key = ec.generate_private_key(ec.SECT163R2())
# Alice_public_key =  binascii.b2a_hex(Alice_private_key.public_key().public_numbers().encode_point()).decode()



Bob_shared_key = Bob_private_key.exchange(ec.ECDH(), Alice_private_key.public_key())
Bob_derived_key = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(Bob_shared_key)
Alice_shared_key = Alice_private_key.exchange(ec.ECDH(), Bob_private_key.public_key())
Alice_derived_key = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(Alice_shared_key)