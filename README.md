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