# -*- codinf:utf-8 -*-
import socket,re,os
import sys
import multiprocessing
import requests


DOCUMENT_ROOT = "./static"

class WSGIServer(object):
    """创建服务器类"""
    def __init__(self, port):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self.tcp_server_socket.bind(("",port))
        self.tcp_server_socket.listen(128)

        self.tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def run_for_server(self):
        '''为客户连接'''
        while True:
            client_socket, client_addr = self.tcp_server_socket.accept()
            print("----->>新用户连接---->>",client_addr)
            # 创建子进程
            # recv_data = client_socket.recv(1024)
            # print(recv_data)
            p1 = multiprocessing.Process(target = self.service_client,args =(client_socket,))
            p1.start()
            
            # 关闭主进程客户端套接字
            client_socket.close()
        # 关闭服务器套接字
        self.tcp_server_socket.close()

    def client(self,send_data):
        # 建立链接
        self.tcp_client_socket.connect(("61.155.164.110",3128))
        # 发送数据
        self.tcp_client_socket.send(send_data.encode("utf-8"))
        recv_data = self.tcp_client_socket.recv(1024*100)

        print(recv_data)
        # 关闭链接s
        # self.tcp_client_socket.close()


    if __name__=="__mian__":
        main()



    def service_client(self, client_socket):
        '''创建为客户服务'''
        while True:
            # print(client_socket)
            recv_data = client_socket.recv(1024)
            # print('----------------------------------------------')
            # print(recv_data)
            # 判断如果没有接收到数据，关闭套接字
            if not recv_data:
                # 关闭客户端套接字
                client_socket.close()
                break

            # 接收浏览器请求的数据
            recv_data = recv_data.decode("utf-8",errors = "ignore")
            print('--------------------recv_data--------------------')
            print(recv_data)
            self.client(recv_data)
            print('--------------------recv_data-end-------------------')
            request_list = recv_data.splitlines()
            # try:
            request_lines = request_list[0]
            # print(66666666666666666666666666)
            # print(request_lines)
            
            ret = re.search(r"(^.*)\s(.*/\s)", request_lines)
            method = ret.group(1)
            url = ret.group(2)
            if method == 'GET':
    

                request_headers = "HTTP/1.1 200 OK\r\n"
                request_headers += "Content-Type:text/html;charset=utf-8\r\n"
                # request_headers += "Content-Length:%d\r\n" % len(response)
                request_headers += "\r\n"
                # 1，发送头部信息
                send_data = request_headers
                client_socket.send(send_data.encode("utf-8"))

                # request_body = response
                # client_socket.send(request_body)
# 
            elif method == 'POST':
                request_body = 'post!'
                client_socket.send(request_body.encode("utf-8"))

            else:
                request_body = 'only suport get and post request!'
                client_socket.send(request_body.encode("utf-8"))

            # client_socket.close()


def main():
    """完成服务器运行流程"""
    port= 7890
    print('server start!  PORT:7890')
    # 创建服务器对象
    server = WSGIServer(port)
    server.run_for_server()


if __name__=="__main__":
    main()