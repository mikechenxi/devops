from http.server import HTTPServer, CGIHTTPRequestHandler
import socket, threading, webbrowser, time


def main():
    port = get_port()
    ip = get_ip()
    start_http_thread = threading.Thread(target=start_http, args=(ip, port,))
    start_http_thread.start()
    check_port_thread = threading.Thread(target=check_port, args=(ip, port,))
    check_port_thread.start()


def get_port():
    port = ''
    while not port.isdigit():
        port = input('请输入共享端口号(小于65535的正整数, 比如80): ')
        if len(port) == 0:
            continue
        elif not port.isdigit() or int(port) > 65535:
            port = ''
            print('端口号需为小于65535的正整数')
        else:
            pass
    return int(port)


def check_port(ip, port):
    print('服务(' + str(port) + ')启动中...')
    service_started = False
    while not service_started:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            service_started = True
        except Exception:
            pass
        s.close()
    print('服务(' + str(port) + ')已启动...')
    show_remind(ip, port)


def show_remind(ip, port):
    url = 'http://' + ip + ':' + str(port)
    print('请在浏览器打开 ' + url + ' 来访问共享文件')
    print('共享目录为本程序所在目录')
    print('直接关掉本窗口即可停止共享')
    time.sleep(1)
    webbrowser.open(url)


def start_http(ip, port):
    try:
        handler = CGIHTTPRequestHandler
        handler.cgi_directories = ['/cgi-bin', '/htbin']
        server = HTTPServer((ip, port), handler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    main()
