import base64
import network
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import time
import os
from colorama import init, Fore, Back, Style

# ******************** configuring communication channel ********************
pnconfig = PNConfiguration()

pnconfig.publish_key = 'add_your_key_here' # Use pubnub to get keysets
pnconfig.subscribe_key = 'add_your_key_here' # Use pubnub to get keysets
pnconfig.uuid = 'myUniqueUUID'
pnconfig.ssl = True

pubnub = PubNub(pnconfig)

# ************************* importing public key *********************
keyPair = RSA.generate(1024)
f=open("Pubkey1024.pubkey", "r")
pubKey1024=f.read()
pubKey1024=RSA.importKey(pubKey1024)
f.close()

# ******************** information representation ********************
init(autoreset=True)
print(Style.BRIGHT + Back.WHITE + Fore.BLACK +"-- Sender --")
print(Style.BRIGHT + Back.YELLOW + Fore.RED +"-- Sending message to Receiver --")
print(Style.BRIGHT + Back.BLACK + Fore.GREEN +" -- Forming transmission network -- \n(close Graph before sending message)")
network.show_network()

# *********************************************************************************************************************
## Sending msg
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
        print ("from device 2: " + message.message)

## connecting clients
def connect():
    # pubnub.add_listener(MySubscribeCallback())
    # pubnub.subscribe().channels("chan-1").execute()
    ## publish a message
    print("-- Just Input a message to publish anytime -- ")
    while True:
        msg = input("[-] ")
        if msg == 'exit': os._exit(1)
        # encrypting message 1st layer
        encryptor = PKCS1_OAEP.new(pubKey1024)
        msgenc1024 = encryptor.encrypt(msg.encode())

        ################################################
        # sending message
        print(Style.BRIGHT + Fore.BLUE + "[+] Encrypted message being sent: ", msgenc1024)
        finalmsg1024 = base64.b64encode(msgenc1024)
        pubnub.publish().channel("chan-1").message(str(finalmsg1024)).pn_async(my_publish_callback)
        print(Style.BRIGHT + Fore.GREEN +"[!] Message forwarded to NODE_2.")

connect() #connect 1 & 2
