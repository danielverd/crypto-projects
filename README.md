# crypto-projects

A collection of cryptographic projects based on work done in CSC609 Data Security and Cryptography at the University of Miami.
The code in this repository is meant only to demonstrate my understanding of cryptographic concepts. I am in no way asserting that these programs represent a robust cryptographic system. If you are implementing a cryptographic system, please use an already implemented robust cryptographic system.

https://www.schneier.com/crypto-gram/archives/1998/1015.html#cipherdesign

\

### Contents

BozhuAES - a modified version of the AES encryption box found at https://github.com/bozhu/AES-Python. This implementation of AES is used because it does not include the modes of operation, which I will be implementing from scratch.

\

modesOfOperation.py - a module containing the block cipher modes of operation. Each cipher is represented as an object and takes as its single parameter a key in the form of a 16 byte (or 16 character) string. The supported ciphers are [ECBCipher,OFBCipher,CBCCipher,CNTRCipher] and each contains the following functions.

    encrypt(self,plaintext) - receives a bytearray argument plaintext and returns a bytearray containing its encryption by the specified mode of operation.

    decrypt(self,ciphertext) - receives a bytearray argument ciphertext and returns a bytearray containing its decryption by the specified mode of operation OR False if there is a padding error.

The module also includes utility functions, most prominently an implementation of the PKCS padding scheme, pkcsPadding(enc,intext).

\

cbcPaddingAttack.py - a standalone script that simulates the padding oracle attack against the CBC block cipher. The CBC mode of operation is malleable, meaning it is vulnerable to feed-through of changes. The essense of this attack is as follows.

By systematically changing bytes in an encrypted message, the attack can find where the message padding begins. This leaks the length of the message. Then, the attack changes an entire block to simulate a padding of length $n+1$, where n is the actual padding of the message. By finding which delta changes the message into a form that passes the padding check, the attack can reverse-engineer the final byte of the message. Repeat this process until the message is broken. The attack is contained in one function: 

    attack(cbc,ciphertext) -  decrypts the ciphertext without using the cbc.decrypt() function

\

