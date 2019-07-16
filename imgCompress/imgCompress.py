#!/usr/bin/python
# -*- coding:utf-8 -*-
# author : b1ng0
import os

path = os.getcwd()
# print path
# encode
png2j2k = path + '\\imgCompress\\transcoding\\openjpeg\\bin\\opj_compress.exe -i ' + path + '\\imgCompress\\transcoding\\openjpeg\\bin\\lena.png -o "' + path + '\\imgCompress\\transcoding\\transcoding\\Service Provider\\lena.j2k" -TP R'
j2k2key = 'cd ' + path + '\\imgCompress\\transcoding\\transcoding && transcoding.exe 1 lena.j2k enc.j2k lena.key'

# print png2j2k
# print j2k2key

# decode
j2k2part = 'cd ' + path + '\\imgCompress\\transcoding\\transcoding && transcoding.exe 2 enc.j2k part.j2k 3'
part2dec = 'cd ' + path + '\\imgCompress\\transcoding\\transcoding && transcoding.exe 3 part.j2k dec.j2k lena.key'
j2k2png = path + '\\imgCompress\\transcoding\\openjpeg\\bin\\opj_decompress.exe -i "' + path + '\\imgCompress\\transcoding\\transcoding\\Client\\dec.j2k" -o ' + path + '\\imgCompress\\transcoding\\transcoding\\Client\\lena.png'


# lena.png -> part.j2k lena.key
def img_encode():
    if os.system(png2j2k) == 0:
        if os.system(j2k2key) == 0:
            if os.system(j2k2part) == 0:
                return 0
    return 1

# part.j2k lena.key -> lena.png
def img_decode():
    if os.system(part2dec) == 0:
        if os.system(j2k2png) == 0:
            return 0
    return 1

# if __name__ == '__main__':
#     img_encode()
#     img_decode()
