import base64

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time
import os
from colorama import init, Fore, Back, Style
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# ******************** configuring communication channel ********************
pnconfig34 = PNConfiguration()

pnconfig34.publish_key = 'add_your_key_here'
pnconfig34.subscribe_key = 'add_your_key_here'
pnconfig34.uuid = 'myUniqueUUID'
pnconfig34.ssl = True

pubnub = PubNub(pnconfig34)

# ****************** Importing private keys ***************
f=open("Privkey1024.privkey", "rb")
priKey1024=RSA.importKey(f.read())
f.close()
f=open("Privkey2048.privkey", "rb")
priKey2048=RSA.importKey(f.read())
f.close()
f=open("Privkey3072.privkey", "rb")
priKey3072=RSA.importKey(f.read())
f.close()

# ******************** information representation ********************
init(autoreset=True)
print(Style.BRIGHT + Back.WHITE + Fore.BLACK +"-- Receiver --")
print(Style.BRIGHT + Back.YELLOW + Fore.RED +"-- Receiving message from Sender --")

# *************************************** Connecting 3 & 4 **********************************************************
## Sending message
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass

## Receiving msg
class MySubscribeCallback(SubscribeCallback):

    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        # receiving message
        msg = message.message
        # string to bytes
        msgbyte = msg.encode()
        msgback = msgbyte[2:514]
        bytestr = base64.b64decode(msgback)
        print(Style.BRIGHT + Fore.BLUE + "[+] Received from NODE 1 through NODE 2,3 received.\n[*] "+msg)

        # Decryption layer 1
        print(Style.BRIGHT + Back.WHITE + Fore.BLACK +"[-] Decrypting 1st layer RSA 3072 -")
        decryptor3072 = PKCS1_OAEP.new(priKey3072)
        decrypted3072 = decryptor3072.decrypt(bytestr)
        print(Style.BRIGHT + Fore.GREEN +"[*] Got: ", decrypted3072)

        # Decryption layer 2
        print(Style.BRIGHT + Back.WHITE + Fore.BLACK + "[-] Decrypting 2nd layer RSA 2048 -")
        decryptor2048 = PKCS1_OAEP.new(priKey2048)
        decrypted2048 = decryptor2048.decrypt(decrypted3072)
        print(Style.BRIGHT + Fore.GREEN + "[*] Got: ", decrypted2048)

        # Decryption layer 3
        print(Style.BRIGHT + Back.WHITE + Fore.BLACK + "[-] Decrypting 3rd layer RSA 1024 -")
        decryptor1024 = PKCS1_OAEP.new(priKey1024)
        decrypted1024 = decryptor1024.decrypt(decrypted2048)
        print(Style.BRIGHT + Fore.GREEN + "[*] Got: ", decrypted1024)

        ############### Final Message ################
        print(Style.BRIGHT + Back.YELLOW + Fore.RED +"[+] Message Received :"+str(decrypted1024))


## connecting clients
def connect():
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels("chan-1").execute()

    ## publish a message
    # while True:
    #     msg = input("Input a message to publish: ")
    #     if msg == 'exit': os._exit(1)
    #     pubnub.publish().channel("chan-1").message(str(msg)).pn_async(my_publish_callback)

connect() # connect 3 & 4
