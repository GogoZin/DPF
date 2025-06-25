# ⚡ DPF - The Most Powerful CC Stress Test Tool of 2025  
![License](https://img.shields.io/badge/license-MIT-green)  
> 🛡️ **DPF** (short for **D**istributed **P**roxies **F**lood) is a **blazing fast CC ATTACK stress-testing tool** built for 2025.  
> It mimics real user requests to help you test your website’s resistance under pressure.

---
>            ╔╦╗┬┌─┐┌┬┐┬─┐┬┌┐ ┬ ┬┌┬┐┌─┐┌┬┐                     
>             ║║│└─┐ │ ├┬┘│├┴┐│ │ │ ├┤  ││                     
>            ═╩╝┴└─┘ ┴ ┴└─┴└─┘└─┘ ┴ └─┘─┴┘                     
>          ╔═╗┬─┐┌─┐─┐ ┬┬ ┬  ╔═╗┬  ┌─┐┌─┐┌┬┐
>          ╠═╝├┬┘│ │┌┴┬┘└┬┘  ╠╣ │  │ ││ │ ││
>          ╩  ┴└─└─┘┴ └─ ┴   ╚  ┴─┘└─┘└─┘─┴┘

![image](https://github.com/GogoZin/DPF/blob/main/image.png)

## 🚀 Features

- 🔹 **Fully Simulated Request Headers**  
 Acts just like a real browser with fake IP support — super realistic and effective.

- 🔹 **Ultra-Fast Proxy Checker**  
 The fastest and most accurate proxy checker out there. Save time, stress less.

- 🔹 **Beginner-Friendly**  
 Simple commands and options. Even complete newbies can launch powerful tests quickly.

- 🔹 **Bypass-Ready**  
 Designed to follow major protection services like Cloudflare — helps sneak through filters.

- 🔹 **High Stability**  
 Multithreaded with solid memory handling — **no core dumps here**!

- 🔹 **Modular & Extendable**  
 Easy to add more attack methods later thanks to its modular design.

---

## 🖥️ System Requirements

| Item         | Recommended Setup   |
|--------------|---------------------|
| CPU          | 4 cores or more     |
| Memory       | 8 GB or more        |
| Network Speed| At least 100 Mbps   |

---

## 📦 Installation

### ✅ Clone the project
```bash
git clone https://github.com/GogoZin/DPF
cd DPF
```

### 🐧 Install on Linux
```bash
pip3 install -r requirements.txt
```

### 🧊 Install on Windows
```bash
py -m pip install -r requirements.txt
```

## 🏃 How to Use

### 🐧 On Linux
```bash
python3 dpf.py <GET/POST/HEAD> <host> <port> <threads> <path> <http/http2> <args>
```

### 🧊 On Windows
```bash
py dpf.py <GET/POST/HEAD> <host> <port> <threads> <path> <http/http2> <args>
```

### ✅ Example
```bash
python3 dpf.py GET example.com 443 500 / http --fetch
```
---

## 📜 License

This project is licensed under the [MIT License](LICENSE)。

---

## ⚠️ Rules & Disclaimer

> 📌 Heads up: This tool is only for developers learning or doing legal performance testing.
>  
> ❌ Don’t use it for any illegal activities (e.g., DDoS attacks or unauthorized testing).
> 
> 📄 By using this tool, you agree to the rules above and the MIT license terms.
> 
> ⚖️ The author is not responsible for any misuse or consequences.
> 
> 🙅 If you don’t agree with the rules — don’t download or use it.

---

## 🌟 Support the Project

Thanks for checking out DPF! Feel free to star ⭐ this repo if you find it useful!
