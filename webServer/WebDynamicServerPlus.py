# -*- coding=utf8 -*-
import re
import sys
import socket
import time
from multiprocessing import Process

DOCUMENT_ROOT = '/Users/nobita/Desktop/pyTest/webServer'
PYTHON_ROOT = '/Users/nobita/Desktop/pyTest/webServer'
server_addr = (HOST, PORT) = '', 8888


class WISGServer(object):
    '''服务器'''
    addressFamily = socket.AF_INET
    addressType = socket.SOCK_STREAM
    requestNum = 10

    def __init__(self, server_addr):
        # 创建tcp套接字
        self.serverSocket = socket.socket(self.addressFamily, self.addressType)
        # 设置端口重用
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # 绑定地址
        self.serverSocket.bind(server_addr)
        # 监听
        self.serverSocket.listen(self.requestNum)

        self.serverName = 'localhost'
        self.serverPort = server_addr[1]

    def setup(self, application):
        '''设置应用'''
        self.application = application

    def run(self):
        '''启动服务器'''
        while True:

            self.clientSocket, client_addr = self.serverSocket.accept()

            # 创建进程
            newClientProcessing = Process(target=self.handleClient)
            newClientProcessing.start()

            self.clientSocket.close()

    def handleClient(self):

        self.recvData = self.clientSocket.recv(1024)

        requestHeaderLines = self.recvData.splitlines()
        for header in requestHeaderLines:
            print header

        requestHeaderFirst = requestHeaderLines[0]
        filename = re.match(r'[^/]+(/[^ ]*)', requestHeaderFirst).group(1)

        if filename[-3:] != '.py':
            if filename == '/':
                file_path = DOCUMENT_ROOT + '/index.html'
            else:
                file_path = DOCUMENT_ROOT + filename

            try:
                file = open(file_path, 'r')
            except IOError as error:
                responseHeader = 'HTTP/1.1 404 not found\r\n'
                responseHeader += '\r\n'
                responseBody = 'so sad! file is not found'
            else:
                responseHeader = 'HTTP/1.1 200 OK\r\n'
                responseHeader += '\r\n'
                responseBody = file.read()
                file.close()

            finally:
                response = responseHeader + responseBody
                self.clientSocket.send(response)
                self.clientSocket.close()
        else:
            # 处理请求头
            self.parseRequest()
            env = self.getenv()

            bodyContent = self.application(env, self.startResponse)

            self.finishResponse(bodyContent)

    def finishResponse(self, bodyContent):
        '''发送请求'''

        status, response_header = self.header_set
        response = 'HTTP/1.1 {status}\r\n'.format(status=status)

        for header in response_header:
            response += '{0}: {1}\r\n'.format(*header)

        response += "\r\n"

        for data in bodyContent:
            response += data

        self.clientSocket.send(response)
        self.clientSocket.close()

    def startResponse(self, status, response_header):
        server_header = [
            ("Data", time.ctime()),
            ("Server", "NServer")
        ]

        self.header_set = [status, server_header + response_header]

    def getenv(self):
        env = {}

        env['wsgi.version'] = (1, 0)
        env['wsgi.input'] = self.recvData
        env['REQUEST_METHOD'] = self.requestMethod
        env['PATH_INFO'] = self.path

        return env

    def parseRequest(self):
        requestHeaderLine = self.recvData.splitlines()[0]
        requestHeaderLine = requestHeaderLine.rstrip('\r\n')
        self.requestMethod, self.path, self.requestVersion = requestHeaderLine.split(' ')


def makeServer(server_addr, application):
    server = WISGServer(server_addr)
    server.setup(application)
    print("WISG服务器启动了，在监听%d端口呐" %PORT)
    server.run()


def main():

    if len(sys.argv) < 2:
        sys.exit("格式不对哦，请参照modual:application")

    appPath = sys.argv[1]

    # 分割出modual,application
    modual, application = appPath.split(':')

    # 导入模块
    modual = __import__(modual)
    # 动态获得application
    application = getattr(modual, application)
    # 生成服务器
    makeServer(server_addr, application)


if __name__ == '__main__':
    main()