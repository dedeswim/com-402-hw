import binascii
import asyncio
import websockets
from hashlib import sha256
import os

def bytes_to_int(x):
    return int.from_bytes(x, 'big')

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

async def pake():
    
    # Constants
    EMAIL = "your.email@epfl.ch"
    PASSWORD = "correct horse battery staple"
    RANDOM_LENGTH = 32
    N = int("EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3",16)
    g = 2

    uri = 'ws://127.0.0.1:5000/'
    async with websockets.connect(uri) as websocket:
        # Send email
        await websocket.send(EMAIL.encode())
        
        # Wait for salt
        utf8_hex_salt = await websocket.recv()
        bigendian_salt = binascii.unhexlify(utf8_hex_salt)
        salt = bytes_to_int(bigendian_salt)
        print("[-] Received salt : " + str(salt))

        # Create and send A
        a = bytes_to_int(os.urandom(RANDOM_LENGTH))
        A = pow(g, a, N)
        bigendian_A = int_to_bytes(A)
        utf8_hex_A = binascii.hexlify(bigendian_A).decode()
        await websocket.send(utf8_hex_A)
        print("[-] Sent A : " + str(A))

        # Wait for B and decode it
        utf8_hex_B = await websocket.recv()
        bigendian_B = binascii.unhexlify(utf8_hex_B)
        B = bytes_to_int(bigendian_B)
        print("[-] Received B : " + str(B))

        # Create H(A || B)
        h_u = sha256()
        h_u.update(int_to_bytes(A))
        h_u.update(int_to_bytes(B))
        u = bytes_to_int(h_u.digest())
        print("[-] u : " + str(u))

        # Create H(salt || H(U || ":" || PASSWORD))
        h_email_psw = sha256()
        h_email_psw.update(EMAIL.encode())
        h_email_psw.update(':'.encode())
        h_email_psw.update(PASSWORD.encode())
        print("[-] H(U || \":\" || PASSWORD) : " + binascii.hexlify(h_email_psw.digest()).decode())
        
        h_x = sha256()
        h_x.update(int_to_bytes(salt))
        h_x.update(h_email_psw.digest())
        x = bytes_to_int(h_x.digest())
        print("[-] H(salt || H(U || \":\" || PASSWORD)) : " + binascii.hexlify(h_x.digest()).decode())
        print("[-] x : " + str(x))
    
        # Compute secret
        S = pow(B - pow(g, x, N), a + (u * x), N)
        print("[-] Secret : " + str(S))

        # Send S to the server
        h_result = sha256()
        h_result.update(int_to_bytes(A))
        h_result.update(int_to_bytes(B))
        h_result.update(int_to_bytes(S))

        result = h_result.digest()
        utf8_hex_result = binascii.hexlify(result).decode()
        
        await websocket.send(utf8_hex_result)

        result = await websocket.recv()
        print(result)
        


asyncio.get_event_loop().run_until_complete(pake())