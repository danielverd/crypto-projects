import string
import sys
import os
import argparse

from BozhuAES import AES

args_g = 0

BLOCK_SIZE = 16  # the AES block size
KEY_SIZE = 16    # the AES key size

def blocks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def pkcsPadding(enc,intext):
    outtext = intext

    if enc:
        padLen = BLOCK_SIZE - (len(outtext) % BLOCK_SIZE)
        for _ in range(padLen):
            outtext = outtext + bytes([padLen])
        return outtext
    
    else:
        #undo padding, also acts as a padding oracle for the padding oracle attack
        pkcsVal = outtext[len(outtext)-1]
        count = 0
        for i in reversed(outtext):
            if count >= pkcsVal:
                return outtext
            if i == pkcsVal:
                del outtext[len(outtext)-1]
                count += 1
            else:
                #padding error simulated by a false boolean
                return False

def delist(text):
    message = bytearray()

    for i in text:
        for item in i:
            message.append(item)
    return message

class ECBCipher():

    def __init__(self,key):
        self.aes = AES(bytes(key,'utf-8'))
    
    def encrypt(self,plaintext):
        plaintext = pkcsPadding(True,plaintext)

        plaintext = blocks(plaintext,BLOCK_SIZE)
        ciphertext = []
        for block in plaintext:
            ciph = self.aes.encrypt_block(block)
            ciphertext.append(ciph)
        
        ciphertext = delist(ciphertext)
        return ciphertext

    def decrypt(self,ciphertext):
        ciphertext = blocks(ciphertext,BLOCK_SIZE)
        plaintext = []
        for block in ciphertext:
            mesg = self.aes.decrypt_block(block)
            plaintext.append(mesg)
        
        plaintext = delist(plaintext)
        plaintext = pkcsPadding(False,plaintext)
        return plaintext

class OFBCipher():

    def __init__(self,aes):
        self.aes = aes
    
    def encrypt(self):
        pass

    def decrypt(self):
        pass

class CBCCipher():
    
    def encrypt(self):
        pass

    def decrypt(self):
        pass

class CNTRCipher():
    
    def encrypt(self):
        pass

    def decrypt(self):
        pass

if __name__ == "__main__":
    key = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'
    text = bytearray('go canes','utf-8')

    ecb = ECBCipher(key)
    encrypted = ecb.encrypt(text)

    print('-----Object Tests-----')
    print('--ECB Cipher--')
    print(text == ecb.decrypt(encrypted))
