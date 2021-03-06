# 2.怎样完成下载？
#   1.创建一个空文件
#   2.向里面写数据
#   3.关闭
# 什么叫上传
# -*- coding:utf-8 -*-

import _struct
import sys
from _socket import *

if len(sys.argv) != 2:
    print('-' * 30)
    print("tips:")
    print("python xxx.py 192.168.1.1")
    print('-' * 30)
    exit()
else:
    ip = sys.argv[1]

# 创建udp套接字
udpSocket = socket(AF_INET, SOCK_DGRAM)

# 构造下载请求数据
sendData = _struct.pack("!H8sb5sb", 1, "test.jpg", 0, "octet", 0)

# 发送下载文件请求数据到指定服务器
sendAddr = (ip, 69)
udpSocket.sendto(sendData, sendAddr)

p_num = 0

recvFile = ''

while True:
    recvData, recvAddr = udpSocket.recvfrom(1024)

    recvDataLen = len(recvData)

    cmdTuple = _struct.unpack("!HH", recvData[:4])

    cmd = cmdTuple[0]
    currentPackNum = cmdTuple[1]

    if cmd == 3:  # 是否为数据包

        # 如果是第一次接收到数据，那么就创建文件
        if currentPackNum == 1:
            recvFile = open("test.jpg", "a")

        # 包编号是否和上次相等
        if p_num + 1 == currentPackNum:
            recvFile.write(recvData[4:]);
            p_num += 1
            print("(%d)次接收到的数据" % p_num)

            ackBuf = _struct.pack("!HH", 4, p_num)
            udpSocket.sendto(ackBuf, recvAddr)

        # 如果收到的数据小于516则认为出错
        if recvDataLen < 516:
            recvFile.close()
            print("已经成功下载")
            break

        elif cmd == 5:
            print("error num:%d" % currentPackNum)
            break

    udpSocket.close()

udpSocket.close()
