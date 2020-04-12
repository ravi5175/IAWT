# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:23:34 2020
Project-Image_Authentication_Using_Water_Marking_Technique
Section-Key_I/0
@author: RAVI
"""

import sys
import math
import itertools
import random
from PIL import Image
    
def shuffle_order(size, shuffle_seed):
    order = []
    for i in range (size):
        order.append(i)
    if (shuffle_seed):
        random.seed(shuffle_seed)
        shuffled = random.shuffle(order)
        return order
    else:
        return order
    
def encrypt(plain, key):
    cipher = []
    k = 0
    len_key = len(key)
    len_plain = len(plain)
    for i in range(len_plain):
        cipher.append((plain[i] + ord(key[i % len_key])) % 256)
    return cipher

def decrypt(cipher, key):
    plain = []
    k = 0
    len_key = len(key)
    len_cipher = len(cipher)
    for i in range(len_cipher):
        plain.append((cipher[i] + 256 - ord(key[i % len_key])) % 256)
    return plain