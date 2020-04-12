# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:23:34 2020
Project-Image Authentication Using Water Marking Technique
Section-Image I/0
@author: RAVI
"""

import cv2
import os
from matplotlib import pyplot as plt
import sys
import math
import itertools
import random
import key_io as skey
from PIL import Image

UPLOAD_FOLDER='/image/upload'
ALLOWED_EXTENSIONS={'png','jpg','jpeg','gif'}


def readLSB(image, width, binary, order):
    bit = []
    px = image.load()
    k = 0
    cur = 0
    for pos in order:
        i = pos / width
        j = pos % width
        if (binary):
            cur |= (px[i % image.width, j % image.height] & 1) << k
        else:
            cur |= (px[i % image.width, j % image.height][0] & 1) << k
        k += 1
        if (k >= 8):
            bit.append(cur)
            k = 0
            cur = 0
    if (k > 0):
        bit.append(cur)
    return bit

def extract_lsb(inputpath, outputpath,key):
    cover = Image.open(inputpath)
    lsb = Image.new("1", cover.size);
    px_cover = cover.load()
    px_lsb = lsb.load()

    #key = input("Enter Key: ")
    seed = 0
    key_size = len(key)
    for i in range(key_size):
        seed += ord(key[i])
    cipher = readLSB(cover, cover.width, 0, key.shuffle_order(cover.width * cover.height, seed))
    plain = skey.decrypt(cipher, key)

    k = 0
    cur = 0
    positions = skey.shuffle_order(cover.width * cover.height, 0)
    for pos in positions:
        i = pos / cover.width
        j = pos % cover.width
        px_lsb[i, j] = ((plain[int(k / 8)] >> (k % 8)) & 1)
        k = (k + 1)
    lsb.save(outputpath);
    lsb.show();

def insert_lsb(inputpath, watermarkpath, outputpath, key):
    cover = Image.open(inputpath)
    watermark = Image.open(watermarkpath).convert("1")
    output = Image.new(cover.mode, cover.size)
    px_cover = cover.load()
    px_watermark = watermark.load()
    px_output = output.load()
    plain = readLSB(watermark, cover.width, 1, skey.shuffle_order(cover.width * cover.height, 0))
    #key = input("Enter Key: ")
    cipher = skey.encrypt(plain, key)
    
    k = 0
    cur = 0
    mod = watermark.width * watermark.height
    seed = 0
    key_size = len(key)
    for i in range(key_size):
        seed += ord(key[i])
    positions = skey.shuffle_order(cover.width * cover.height, seed)
    for pos in positions:
        i = pos / cover.width
        j = pos % cover.width
        p = list(px_cover[i, j])
        p[0] = (p[0] & 0b11111110) | ((cipher[int(k / 8)]>>(k % 8)) & 1)
        k = (k + 1) % mod
        px_output[i, j] = tuple(p)
    output.save(outputpath)
    output.show()    


def psnr(watermarkedcover, plaincover):
    return 20 * math.log10(255/skey.rms(watermarkedcover, plaincover))


def print_psnr(watermarkedpath, plainpath):
    watermarked = Image.open(watermarkedpath)
    plain = Image.open(plainpath)

    print("PSNR: " + str(psnr(watermarked, plain)))     
