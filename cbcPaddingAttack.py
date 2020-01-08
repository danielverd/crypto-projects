from modesOfOperation import CBCCipher

BLOCK_SIZE = 16

def blocks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def attack(cbc,ciphertext):
    return False

if __name__ == "__main__":
    key = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'
    text = bytearray('go canes','utf-8')

    cbc = CBCCipher(key)
    ciphertext = cbc.encrypt(text)

    broken = attack(cbc,ciphertext)

    print('-----Equality between text and broken message-----')
    print(broken == text)
    