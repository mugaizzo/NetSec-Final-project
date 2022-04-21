import pyDH
d1 = pyDH.DiffieHellman(group=5)
d2 = pyDH.DiffieHellman(group=5)

d1_pubkey = d1.gen_public_key()
d2_pubkey = d2.gen_public_key()
print(d1_pubkey)
# print(d2_pubkey)

d1_sharedkey = d1.gen_shared_key(d2_pubkey)
d2_sharedkey = d2.gen_shared_key(d1_pubkey)
d1_sharedkey == d2_sharedkey


# print(d2_pubkey)
# print(d2_sharedkey)
