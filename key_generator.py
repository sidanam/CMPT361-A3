#!/bin/python3
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

KeyLen = 256
print(get_random_bytes(int(KeyLen/8)))
