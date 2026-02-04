import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# ===== KONFIGURASI =====
EDGE_DRIVER_PATH = "./driver/msedgedriver.exe"
SEARCH_URL = "https://www.bing.com"
REFRESH_INTERVAL = 7  # detik

# Daftar keyword yang lebih banyak
keywords = [
    "warren buffet portfolio",
    "saham hari ini naik apa",
    "harga emas antam hari ini",
    "python selenium edge webdriver",
    "contoh script python automation",
    "cara web scraping python",
    "tutorial data science pemula",
    "machine learning untuk pemula",
    "apa itu artificial intelligence",
    "tips belajar coding cepat",
    "best practice coding",
    "belajar software development",
    "library python populer",
    "tools automation terbaik",
    "perkembangan teknologi terbaru",
    "berita terbaru hari ini",
    "resep masakan sederhana",
    "tips hidup sehat",
    "tutorial fotografi pemula",
    "cara belajar bahasa inggris cepat"
]

# ===== SETUP EDGE =====
print("Memulai Edge browser...")
options = Options()

options.add_argument("user-data-dir=C:\\Users\\krido\\AppData\\Local\\Microsoft\\Edge\\User Data")
options.add_argument("profile-directory=Profile 13")

# Hilangkan deteksi automation/bot banner
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Tambahan agar lebih natural
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")

service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

# Hapus properti webdriver untuk menghindari deteksi bot
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 10)

# Buka mesin pencari
driver.get(SEARCH_URL)
print(f"Browser terbuka di {SEARCH_URL}\n")

# ===== LOOP SEARCH TERUS-MENERUS =====
search_count = 0

try:
    while True:  # Loop tanpa batas
        # Pilih keyword random
        keyword = random.choice(keywords)
        
        # Buat keyword unik dengan timestamp
        unique_keyword = f"{keyword} {datetime.now().strftime('%H%M%S')}"
        
        try:
            # Tunggu dan cari search box
            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # Clear dan ketik keyword baru
            search_box.clear()
            search_box.send_keys(unique_keyword)
            search_box.send_keys(Keys.ENTER)
            
            search_count += 1
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{current_time}] Search #{search_count}: {unique_keyword}")
            
            # Tunggu 7 detik
            time.sleep(REFRESH_INTERVAL)
            
            # Refresh halaman untuk search berikutnya
            driver.refresh()
            print(f"  → Refresh halaman...")
            time.sleep(1)  # Tunggu sebentar setelah refresh
            
        except Exception as e:
            print(f"Error saat search: {e}")
            print("Mencoba kembali ke halaman utama...")
            driver.get(SEARCH_URL)
            time.sleep(2)
            continue

except KeyboardInterrupt:
    print(f"\n\n{'='*50}")
    print("Script dihentikan manual")
    print(f"Total pencarian yang dilakukan: {search_count}")
    print(f"{'='*50}")

except Exception as e:
    print(f"\nError tidak terduga: {e}")

finally:
    print("\nMenutup browser...")
    driver.quit()
    print("Selesai!")