            ╔╦╗┬┌─┐┌┬┐┬─┐┬┌┐ ┬ ┬┌┬┐┌─┐┌┬┐                     
             ║║│└─┐ │ ├┬┘│├┴┐│ │ │ ├┤  ││                     
            ═╩╝┴└─┘ ┴ ┴└─┴└─┘└─┘ ┴ └─┘─┴┘                     
          ╔═╗┬─┐┌─┐─┐ ┬┬ ┬  ╔═╗┬  ┌─┐┌─┐┌┬┐
          ╠═╝├┬┘│ │┌┴┬┘└┬┘  ╠╣ │  │ ││ │ ││
          ╩  ┴└─└─┘┴ └─ ┴   ╚  ┴─┘└─┘└─┘─┴┘

# DPF - Distributed Proxy Flood


DPF use lots of socks5 proxy for request,
and support http2, so you can bypass more cdn and WAF 
---------------------------------------------------------------------------------------------
Install on Linux
```
sudo apt-get update
sudo apt-get install python3 python3-pip git
git clone https://github.com/GogoZin/DPF
cd DPF
```

Module install
```
python3 -m pip install requests pysocks h2
```
Or 
```
pip3 install requests pysocks h2
```

Windows , download and install Python3 here -> https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tar.xz

After installed, download this tool as ZIP file and extract

Open your CMD and input

```
cd DPF
py -m pip install requests pysocks h2 bs4
py dpf.py
```

NOTE: 
--------------------------------------------------------------
API for proxy in this script is suck, 
use your own proxy list if you want more performance 
--------------------------------------------------------------
