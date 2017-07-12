# -*- coding=utf8 -*-
import sys
import socket
import struct


def upload(udpsocket, sendAddr, filename):
    '''上传文件'''
    i = 0
    packNum = 0
    uploadFile = None

    # 组装上传文件请求
    upload_request = struct.pack("!H%dsb5sb" %len(filename), 2, filename, 0, 'octet', 0)

    # 发送请求
    udpsocket.sendto(upload_request, sendAddr)

    while True:
        # 接受数据
        recvData, recvAddr = udpsocket.recvfrom(1024)

        cmdTuple = struct.unpack("!HH", recvData[:4])

        cmd = cmdTuple[0]
        currentPackNum = cmdTuple[1]

        if cmd == 4:
            try:
                # 读取等待上传文件
                uploadFile = open("test.pdf", 'r')
                uploadFile.seek(i*512, 0)
                content = uploadFile.read(512)
                i += 1
                uploadFile.close()

                if packNum == currentPackNum:

                    # 组包
                    udpcontent = struct.pack("!HH%ss" %len(content), 3, currentPackNum+1, content)
                    udpsocket.sendto(udpcontent, recvAddr)
                    packNum += 1
                    print("(%d)次成功上传数据!" %currentPackNum)

                    # 防止文件过大，超出2字节限制
                    if packNum == 65536:
                        packNum = 0

                if len(content) < 512:
                    print "上传完成"
                    break
            except IOError:
                print("本地没有这个文件")
                break
        elif cmd == 5:
            print 'error num %d' %currentPackNum
            print "请重新上传"
            break


def download(udpsocket, sendAddr, filename):
    """下载文件"""

    # 组装下载请求的包
    download_request = struct.pack("!H%dsb5sb" %len(filename), 1, filename, 0, 'octet', 0)
    # 发送请求
    udpsocket.sendto(download_request, sendAddr)

    packNum = 1
    recvFile = None

    while True:
        # 接受返回的数据、地址
        recvData, recvAddr = udpsocket.recvfrom(1024)

        recvDataLen = len(recvData)

        # 解码、查看返回的操作码
        cmdTuple = struct.unpack("!HH", recvData[:4])

        cmd = cmdTuple[0]

        currentPackNum = cmdTuple[1]

        if cmd == 3:

            # 如果是第一个数据包创建文件
            if currentPackNum == 1:
                recvFile = open('test.pdf', 'a')

            # 收到包后发送确认码
            if packNum == currentPackNum:
                recvFile.write(recvData[4:])

                print("(%d)次接受到的数据!" %packNum)
                # 组装确认包
                ack_packet = struct.pack('!HH', 4, packNum)

                # 发送
                udpsocket.sendto(ack_packet, recvAddr)

                packNum += 1
                # 防止文件过大，超出2字节限制
                if packNum == 65536:
                    packNum = 0

            # 收到的数据包小于512结束
            if recvDataLen < 516:
                recvFile.close()
                print "下载成功"
                break
        elif cmd == 5:
            print 'error num %d' %currentPackNum
            print "请重新下载"
            break


def main():

    if len(sys.argv) < 2:
        print("格式: python xx.py pull:127.0.0.1:test.pdf")
        return
    data = sys.argv[1].split(":")

    IP = data[1]
    OPERATOR = data[0]
    filename = data[2]
    # 创建udp套接字
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 发送的地址
    sendAddr = (IP, 69)

    if OPERATOR in ("PULL", "pull"):
        download(udpsocket, sendAddr, filename)
    elif OPERATOR in ('PUT', 'put'):
        upload(udpsocket, sendAddr, filename)
    else:
        print("没有该命令")
    udpsocket.close()

if __name__ == '__main__':
    main()
