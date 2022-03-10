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
pnconfig23 = PNConfiguration()
pnconfig34 = PNConfiguration()
 
pnconfig23.publish_key = 'add_your_key_here' # use key set used in First_Node.py here
pnconfig23.subscribe_key = 'add_your_key_here' # use key set used in First_Node.py here
pnconfig23.uuid = 'myUniqueUUID'
pnconfig23.ssl = True
pnconfig34.publish_key = 'add_your_key_here' # use key set used in Receiver.py here
pnconfig34.subscribe_key = 'add_your_key_here'  # use key set used in Receiver.py here
pnconfig34.uuid = 'myUniqueUUID'
pnconfig34.ssl = True

pubnub23 = PubNub(pnconfig23)
pubnub34 = PubNub(pnconfig34)

# ************************* importing public key *********************
keyPair = RSA.generate(3072)
f=open("Pubkey3072.pubkey", "r")
pubKey3072=f.read()
pubKey3072=RSA.importKey(pubKey3072)
f.close()

# ******************** information representation ********************
init(autoreset=True)
f=open("client_2.txt",'r')
name=f.read()
f.close()
print(Style.BRIGHT + Back.WHITE + Fore.BLACK+"-- "+name+" --")
print(Style.BRIGHT + Back.BLACK + Fore.YELLOW +"-- Relay Node between Sender & Receiver --")

# *************************************** Connecting 2 & 3 **********************************************************
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
        chan23 = message.message
        print (Style.BRIGHT + Fore.BLUE +"[+] received from Sender to Receiver through Relay Node." )
        connect_3_4(chan23)

## connecting clients
def connect_2_3():
    pubnub23.add_listener(MySubscribeCallback())
    pubnub23.subscribe().channels("chan-1").execute()

    ## publish a message
    # while True:
    #     msg = input("-- Just Input a message to publish anytime -- \n")
    #     if msg == 'exit': os._exit(1)
    #     pubnub.publish().channel("chan-2").message(str(msg)).pn_async(my_publish_callback)

# *************************************** Connecting 3 & 4 **********************************************************
## Sending message
def my_publish_callback_3_4(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass

## Receiving msg
class MySubscribeCallback_3_4(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
    def status(self, pubnub, status):
        pass
    def message(self, pubnub, message):
        print ("from device 3: " + message.message)

## connecting clients
def connect_3_4(chan23):
    # for listening
    # pubnub23.add_listener(MySubscribeCallback_2_3())
    # pubnub23.subscribe().channels("chan-2").execute()

    ## publish a message
    try:
        msg34 = chan23
        # string to bytes
        msgbyte = msg34.encode()
        msgback = msgbyte[2:346]
        bytestr = base64.b64decode(msgback)
        print("[-] "+msg34)
        print("**************************************************************************")
        if msg34 == 'exit': os._exit(1)
        ##############################################

        # encrypting message 3rd layer
        encryptor = PKCS1_OAEP.new(pubKey3072)
        msgenc3072 = encryptor.encrypt(bytestr)
        finalmsg3072 = base64.b64encode(msgenc3072)
        #############################################

        # sending message
        print(Style.BRIGHT + Fore.RED + "[+] Encrypted message being sent: ", msgenc3072)
        pubnub34.publish().channel("chan-1").message(str(finalmsg3072)).pn_async(my_publish_callback_3_4)
        print(Style.BRIGHT + Fore.GREEN +"[!] Message forwarded to Receiver.")
    except NameError:
        pass

connect_2_3()
