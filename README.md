            ╔╦╗┬┌─┐┌┬┐┬─┐┬┌┐ ┬ ┬┌┬┐┌─┐┌┬┐                     
             ║║│└─┐ │ ├┬┘│├┴┐│ │ │ ├┤  ││                     
            ═╩╝┴└─┘ ┴ ┴└─┴└─┘└─┘ ┴ └─┘─┴┘                     
          ╔═╗┬─┐┌─┐─┐ ┬┬ ┬  ╔═╗┬  ┌─┐┌─┐┌┬┐
          ╠═╝├┬┘│ │┌┴┬┘└┬┘  ╠╣ │  │ ││ │ ││
          ╩  ┴└─└─┘┴ └─ ┴   ╚  ┴─┘└─┘└─┘─┴┘

![image](https://github.com/GogoZin/DPF/blob/main/image.png)

# ⚡ DPF - 2025年最強效能的 CC 壓測工具

> 🛡️ **DPF**（**D**istributed **P**roxies **F**lood）是一款為 2025 年打造的 **超高速 CC ATTACK 壓力測試工具**，  
> 通過模擬真實用戶請求，幫助你測試網站的抗壓能力。

---

## 🚀 功能特色

- 🔹 **完整的請求標頭**  
 模擬標準瀏覽器行為 + 偽造 IP，提升真實度與效果。

- 🔹 **極速代理檢測**  
 全網最快速、最精準的代理檢測模組，省時高效。

- 🔹 **新手友好**  
 簡易參數設計，小白也能快速上手壓測。

- 🔹 **遵守主流規則**  
 參考 Cloudflare 等主流防禦規則設計請求結構。

- 🔹 **高穩定性**  
 多執行緒與記憶體管理完善，**不會出現 core dumped**！

- 🔹 **擴充性強**  
 架構模組化，未來可擴增更多攻擊模擬方式。

---

## 🖥️ 系統配置需求

| 項目       | 建議配置        |
|------------|-----------------|
| 處理器     | 4 核心以上      |
| 記憶體     | 8 GB 以上        |
| 網路速度   | 100 Mbps 以上   |

---

## 📦 安裝說明

### ✅ 下載專案
```bash
git clone https://github.com/GogoZin/DPF
cd DPF
```

### 🐧 Linux 安裝模組
```bash
pip3 install -r requirements.txt
```

### 🧊 Windows 安裝模組
```bash
py -m pip install -r requirements.txt
```

## 🏃 使用方式

### 🐧 Linux 執行命令
```bash
py dpf.py <GET/POST/HEAD> <host> <port> <threads> <path> <http/http2> <args>
```

### 🧊 Windows 執行命令
```bash
py dpf.py <GET/POST/HEAD> <host> <port> <threads> <path> <http/http2> <args>
```

### ✅ 範例
```bash
python3 dpf.py GET example.com 443 500 / http --fetch
```
## 📜 授權條款

本專案使用 [MIT License](LICENSE)。

---

## ⚠️ 使用規章

> ⚠️ **請勿濫用此腳本**，此工具僅供開發與安全測試用途。  
>  
> 若您將其用於非法用途，一切後果與作者無關。  
> 下載或使用本專案即表示您同意此規章。不同意者請勿下載或使用。

---

感謝使用 DPF，歡迎 star ⭐ 支持！
