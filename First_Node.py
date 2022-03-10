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
import binascii

# ******************** configuring communication channel ********************
pnconfig12 = PNConfiguration()
pnconfig23 = PNConfiguration()

pnconfig12.publish_key = 'add_your_key_here' # use keyset used in Sender.py here
pnconfig12.subscribe_key = 'add_your_key_here' # use keyset used in Sender.py here
pnconfig12.uuid = 'myUniqueUUID'
pnconfig12.ssl = True
pnconfig23.publish_key = 'add_your_key_here' # use keyset used in Second_Node.py
pnconfig23.subscribe_key = 'add_your_key_here' # use keyset used in Second_Node.py
pnconfig23.uuid = 'myUniqueUUID'
pnconfig23.ssl = True

pubnub12 = PubNub(pnconfig12)
pubnub23 = PubNub(pnconfig23)

# ************************* importing public key *********************
keyPair = RSA.generate(2048)
f=open("Pubkey2048.pubkey", "r")
pubKey2048=f.read()
pubKey2048=RSA.importKey(pubKey2048)
f.close()

# ******************** information representation ********************
init(autoreset=True)
f=open("client_1.txt",'r')
name=f.read()
f.close()
print(Style.BRIGHT + Back.WHITE + Fore.BLACK+"-- "+name+" --")
print(Style.BRIGHT + Back.BLACK + Fore.YELLOW +"-- Relay Node between Sender & Receiver --")

# *************************************** Connecting 1 & 2 **********************************************************
## Sending message
def my_publish_callback_1_2(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass

## Receiving msg
class MySubscribeCallback_1_2(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        chan12=message.message
        print (Style.BRIGHT + Fore.BLUE +"[+] received from NODE 1 for NODE 4.")
        connect_2_3(chan12)

## connecting clients
def connect_1_2():
    pubnub12.add_listener(MySubscribeCallback_1_2())
    pubnub12.subscribe().channels("chan-1").execute()

    ## publish a message
    # while True:
    #     msg12 = input("Input a message to publish: ")
    #     if msg12 == 'exit': os._exit(1)
    #     pubnub12.publish().channel("chan-1").message(str(msg12)).pn_async(my_publish_callback_1_2)

# *************************************** Connecting 2 & 3 **********************************************************
## Sending message
def my_publish_callback_2_3(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass

## Receiving msg
class MySubscribeCallback_2_3(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        print ("from device 3: " + message.message)

## connecting clients
def connect_2_3(chan12):
    # for listening
    # pubnub23.add_listener(MySubscribeCallback_2_3())
    # pubnub23.subscribe().channels("chan-2").execute()

    ## publish a message
    try:
        ## string to bytes
        msg23 = chan12
        msgbyte = msg23.encode()
        msgback = msgbyte[2:174]
        bytestr = base64.b64decode(msgback)
        print("[-] " + msg23)
        print("**************************************************************************")
        if msg23 == 'exit': os._exit(1)
        ##############################################

        ## encrypting message 2nd layer
        encryptor = PKCS1_OAEP.new(pubKey2048)
        msgenc2048 = encryptor.encrypt(bytestr)
        finalmsg2048 = base64.b64encode(msgenc2048)
        ##############################################

        ## sending message
        print(Style.BRIGHT + Fore.RED + "[+] Encrypted message being sent: ", msgenc2048)
        pubnub23.publish().channel("chan-1").message(str(finalmsg2048)).pn_async(my_publish_callback_2_3)
        print(Style.BRIGHT + Fore.GREEN +"[!] Message forwarded to Realy Node.")
    except Exception:
        pass


# connect()
connect_1_2()
