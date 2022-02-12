import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import json

keyPair = RSA.generate(3072)

f=open("PrivateKey.privkey", "rb")
priKey=RSA.importKey(f.read())
f.close()

f=open("PublicKey.pubkey", "rb")
pubKey=RSA.importKey(f.read())
f.close()

msg = 'A message'
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(msg.encode())
print(encrypted)
print("\n")

f=open("cipher.txt", "wb")
f.write(encrypted)
f.close()
f=open("cipher.txt", "rb")
txt=(f.read())
f.close()

decryptor = PKCS1_OAEP.new(priKey)
decrypted = decryptor.decrypt(txt)
print('Decrypted:', decrypted)

#############################################################################################
# REPEATED ENCRYPTION


keyPair3072 = RSA.generate(3072)
keyPair2048 = RSA.generate(2048)
keyPair1024 = RSA.generate(1024)

pubKey1024 = keyPair1024.publickey()
# print(f"Public key in hex:  (n={hex(pubKey1024.n)}, e={hex(pubKey1024.e)})")
pubKeyPEM1024 = pubKey1024.exportKey()
print("Public key 1024: ")
print(pubKeyPEM1024.decode('ascii'))
print("\n")

# print(f"Private key in hex: (n={hex(pubKey1024.n)}, d={hex(keyPair1024.d)})")
privKeyPEM1024 = keyPair1024.exportKey()
print("Private key 1024: ")
print(privKeyPEM1024.decode('ascii'))
print("\n")


msg = 'A message for encryption'
encryptor1024 = PKCS1_OAEP.new(pubKey1024)
encrypted1024 = encryptor1024.encrypt(msg.encode())
print("Encrypted 1024:", str(encrypted1024))
# f = open("demofile2.txt", "a")
# f.write("Now the file has more content!")
# f.close()

#######################################################################################
pubKey2048 = keyPair2048.publickey()
# print(f"Public key in hex:  (n={hex(pubKey2048.n)}, e={hex(pubKey2048.e)})")
pubKeyPEM2048 = pubKey2048.exportKey()
print("Public key 2048: ")
print(pubKeyPEM2048.decode('ascii'))
print("\n")

# print(f"Private key in hex: (n={hex(pubKey2048.n)}, d={hex(keyPair2048.d)})")
privKeyPEM2048 = keyPair2048.exportKey()
print("Private key 2048: ")
print(privKeyPEM2048.decode('ascii'))
print("\n")


msg2048 = encrypted1024
encryptor2048 = PKCS1_OAEP.new(pubKey2048)
encrypted2048 = encryptor2048.encrypt(msg2048)
print("Encrypted 2048:", str(encrypted2048))

#######################################################################################
pubKey3072 = keyPair3072.publickey()
# print(f"Public key in hex:  (n={hex(pubKey3072.n)}, e={hex(pubKey3072.e)})")
pubKeyPEM3072 = pubKey3072.exportKey()
print("Public key 3072: ")
print(pubKeyPEM3072.decode('ascii'))
print("\n")

# print(f"Private key in hex: (n={hex(pubKey3072.n)}, d={hex(keyPair3072.d)})")
privKeyPEM3072 = keyPair3072.exportKey()
print("Private key 3072: ")
print(privKeyPEM3072.decode('ascii'))
print("\n")


msg3072 = encrypted2048
encryptor3072 = PKCS1_OAEP.new(pubKey3072)
encrypted3072 = encryptor3072.encrypt(msg3072)
print("Encrypted 3072:", str(encrypted3072))

#######################################################################################
#######################################################################################
#decryption
decryptor3072 = PKCS1_OAEP.new(keyPair3072)
decrypted3072 = decryptor3072.decrypt(encrypted3072)
print('Decrypted 3072:', decrypted3072)
##########################################################
decryptor2048 = PKCS1_OAEP.new(keyPair2048)
decrypted2048 = decryptor2048.decrypt(decrypted3072)
print('Decrypted 2048:', decrypted2048)
##########################################################
decryptor1024 = PKCS1_OAEP.new(keyPair1024)
decrypted1024 = decryptor1024.decrypt(decrypted2048)
print('Decrypted 2048:', decrypted1024)

