import os
from BozhuAES import AES

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

    def __init__(self,key):
        self.aes = AES(bytes(key,'utf-8'))
    
    def encrypt(self,plaintext):
        plaintext = pkcsPadding(True,plaintext)

        plaintext = blocks(plaintext,BLOCK_SIZE)
        ciphertext = []
        iv = os.urandom(16)
        ciphertext.append(iv)

        interim = self.aes.encrypt_block(ciphertext[0])
        for block in plaintext:
            int_temp = int.from_bytes(interim,'little')
            int_block = int.from_bytes(block,'little')
            int_enc = int_temp ^ int_block

            ciphertext.append(int_enc.to_bytes(BLOCK_SIZE,'little'))
            interim = self.aes.encrypt_block(interim)
        ciphertext = delist(ciphertext)
        return ciphertext

    def decrypt(self,ciphertext):
        ciphertext = blocks(ciphertext,BLOCK_SIZE)
        ciphertext = list(ciphertext)
        plaintext = []
        interim = self.aes.encrypt_block(ciphertext[0])

        for block in ciphertext[1:]:
            int_temp = int.from_bytes(interim,'little')
            int_block = int.from_bytes(block,'little')
            int_enc = int_temp ^ int_block

            plaintext.append(int_enc.to_bytes(BLOCK_SIZE,'little'))
            interim = self.aes.encrypt_block(interim)
        
        plaintext = delist(plaintext)
        plaintext = pkcsPadding(False,plaintext)
        return plaintext

class CBCCipher():

    def __init__(self,key):
        self.aes = AES(bytes(key,'utf-8'))
    
    def encrypt(self,plaintext):
        plaintext = pkcsPadding(True,plaintext)

        plaintext = blocks(plaintext,BLOCK_SIZE)
        ciphertext = []
        iv = os.urandom(16)
        ciphertext.append(iv)
        interim = iv

        for block in plaintext:
            int_temp = int.from_bytes(interim,'little')
            int_block = int.from_bytes(block,'little')
            int_enc = int_temp ^ int_block

            interim = self.aes.encrypt_block(int_enc.to_bytes(BLOCK_SIZE,'little'))
            ciphertext.append(interim)
        ciphertext = delist(ciphertext)
        return ciphertext

    def decrypt(self,ciphertext):
        ciphertext = blocks(ciphertext,BLOCK_SIZE)
        ciphertext = list(ciphertext)
        plaintext = []
        interim = ciphertext[0]

        for block in ciphertext[1:]:
            temp = interim
            interim = block
            decrypted = self.aes.decrypt_block(block)

            int_temp = int.from_bytes(temp,'little')
            int_decr = int.from_bytes(decrypted,'little')
            int_enc = int_temp ^ int_decr
            plaintext.append(int_enc.to_bytes(BLOCK_SIZE,'little'))
        
        plaintext = delist(plaintext)
        plaintext = pkcsPadding(False,plaintext)
        return plaintext

class CNTRCipher():

    def __init__(self,key):
        self.aes = AES(bytes(key,'utf-8'))
    
    def encrypt(self,plaintext):
        plaintext = pkcsPadding(True,plaintext)

        plaintext = blocks(plaintext,BLOCK_SIZE)
        ciphertext = []
        i = 0
        iv = os.urandom(16)
        ciphertext.append(iv)

        ivInt = int.from_bytes(iv,'little')
        for block in plaintext:
            interim = ivInt + i
            temp = self.aes.encrypt_block(interim.to_bytes(BLOCK_SIZE,'little'))
            int_temp = int.from_bytes(temp,'little')
            int_block = int.from_bytes(block,'little')
            int_enc = int_temp ^ int_block

            ciphertext.append(int_enc.to_bytes(BLOCK_SIZE,'little'))
            i += 1
        ciphertext = delist(ciphertext)
        return ciphertext

    def decrypt(self,ciphertext):
        ciphertext = blocks(ciphertext,BLOCK_SIZE)
        ciphertext = list(ciphertext)
        plaintext = []
        i = 0
        iv = ciphertext[0]

        ivInt = int.from_bytes(iv,'little')
        for block in ciphertext[1:]:
            interim = ivInt + i
            temp = self.aes.encrypt_block(interim.to_bytes(BLOCK_SIZE,'little'))
            int_temp = int.from_bytes(temp,'little')
            int_block = int.from_bytes(block,'little')
            int_enc = int_temp ^ int_block

            plaintext.append(int_enc.to_bytes(BLOCK_SIZE,'little'))
            i += 1
        
        plaintext = delist(plaintext)
        plaintext = pkcsPadding(False,plaintext)
        return plaintext

if __name__ == "__main__":
    key = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'
    text = bytearray('go canes','utf-8')

    ecb = ECBCipher(key)
    ofb = OFBCipher(key)
    cbc = CBCCipher(key)
    cntr = CNTRCipher(key)

    print('-----Object Tests-----')
    print('--ECB Cipher--')
    print(text == ecb.decrypt(ecb.encrypt(text)))
    print('--OFB Cipher--')
    print(text == ofb.decrypt(ofb.encrypt(text)))
    print('--CBC Cipher--')
    print(text == cbc.decrypt(cbc.encrypt(text)))
    print('--CNTR Cipher--')
    print(text == cntr.decrypt(cntr.encrypt(text)))

    print('-----Padding Oracle Test-----')
    truePad = cbc.encrypt(text)
    truePad[-1] = 72
    print('--Should Return False--')
    print(cbc.decrypt(truePad))
