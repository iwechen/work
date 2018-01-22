import requests
import socket
# 根据协议类型，选择不同的代理
# proxies = {"http": "http://127.0.0.1:8899"}
# response = requests.get("http://www.baidu.com/", proxies = proxies)
# print(response.text)



def client():
    send_data = '''GET http://www.baidu.com/ HTTP/1.1\r
    Host: www.baidu.com\r
    Connection: keep-alive\r
    Accept: */*\r
    Accept-Encoding: gzip, deflate\r
    User-Agent: python-requests/2.9.1\r\r'''

    tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_client_socket.connect(("61.155.164.110",3128))
    # tcp_client_socket.connect(("127.0.0.1",8899))
    # 发送数据
    tcp_client_socket.send(send_data.encode("utf-8"))
    recv_data = tcp_client_socket.recv(1024)
    tcp_client_socket.close()

    print(recv_data)



if __name__ == '__main__':
    client()

