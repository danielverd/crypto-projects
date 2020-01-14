from modesOfOperation import CBCCipher
import sys

BLOCK_SIZE = 16

def blocks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def attack(cbc,ciphertext):
    message = bytearray(b'')

    blockGen = blocks(ciphertext,BLOCK_SIZE)
    ctextBlocks = []
    for i in blockGen:
        ctextBlocks.append(i)
    
    padBlock = ctextBlocks[len(ctextBlocks)-2]

    for i in range(BLOCK_SIZE):
        padBlock[i] = 72
        if cbc.decrypt(bytearray(b''.join(ctextBlocks))) is False:
            padlength = BLOCK_SIZE - i
            break

    ctextBlocks = []
    blockGen = blocks(ciphertext,BLOCK_SIZE)
    for i in blockGen:
    	ctextBlocks.append(i)
    probeBlocks = ctextBlocks.copy()

    delta1 = bytearray(BLOCK_SIZE)
    for j in range(padlength):
        delta1[BLOCK_SIZE - (1 + j)] = padlength
	
    for i in reversed(range(BLOCK_SIZE - padlength)):
        delta2 = bytearray(BLOCK_SIZE)

        for j in range(BLOCK_SIZE - i):
            delta2[BLOCK_SIZE - (1 + j)] = (BLOCK_SIZE - i)

        for j in range(256):
            cipherInter = probeBlocks.copy()
            delta2[i] = j
            delta = bytearray(bytes([a ^ b for (a,b) in zip(delta1, delta2)]))

            block = cipherInter[len(cipherInter) - 2]
            probe = bytearray(bytes([a ^ b for (a,b) in zip(block, delta)]))
            cipherInter[len(cipherInter) - 2] = probe

            if cbc.decrypt(bytearray(b''.join(cipherInter))) is not False:
                sol1 = (BLOCK_SIZE - i)
                sol2 = j
                sol = sol1 ^ sol2
                delta1[i] = sol
                message = sol.to_bytes(1,'little') + message
                break

    probeBlocks = ctextBlocks.copy()

    while len(probeBlocks)>2:
        probeBlocks = probeBlocks.copy()[:-1]
        delta1 = bytearray(BLOCK_SIZE)

        for i in reversed(range(BLOCK_SIZE)):
            delta2 = bytearray(BLOCK_SIZE)
            for j in range(BLOCK_SIZE - (i+1)):
                delta2[BLOCK_SIZE - (1 + j)] = (BLOCK_SIZE - i)
            
            for j in range(256):
                cipherInter = probeBlocks.copy()
                delta2[i] = j
                delta = bytearray(bytes([a ^ b for (a,b) in zip(delta1, delta2)]))

                block = cipherInter[len(cipherInter)-2]
                probe = bytearray(bytes([a ^ b for (a,b) in zip(block, delta)]))
                cipherInter[len(cipherInter)-2] = probe

            if cbc.decrypt(bytearray(b''.join(cipherInter))) is not False:
                sol1 = BLOCK_SIZE - i
                sol2 = j
                sol = sol1 ^ sol2
                delta1[i] = sol
                message = sol.to_bytes(1,'little') + message

    return message

if __name__ == "__main__":
    key = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15'
    text = bytearray('go canes','utf-8')

    cbc = CBCCipher(key)
    ciphertext = cbc.encrypt(text)
    #print(ciphertext)

    broken = attack(cbc,ciphertext)
    #print(broken)

    print('-----Equality between text and broken message-----')
    print(broken == text)
