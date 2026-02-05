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
EDGE_DRIVER_PATH = "./driver/x64/msedgedriver.exe"
SEARCH_URL = "https://www.bing.com"

# Keyword yang lebih natural dan variatif (topik berbeda)
keywords = [
    "how to invest in stocks for beginners",
    "best programming languages 2025",
    "healthy breakfast recipes",
    "latest technology news",
    "python tutorial for data analysis",
    "best laptops under 1000 dollars",
    "how to improve productivity at work",
    "travel destinations southeast asia",
    "machine learning projects ideas",
    "home workout routines",
    "digital marketing strategies",
    "best books to read 2025",
    "climate change solutions",
    "how to start a podcast",
    "photography tips for beginners",
    "web development frameworks comparison",
    "financial planning tips",
    "meditation techniques for stress",
    "sustainable living ideas",
    "career development advice"
]

# ===== FUNGSI HELPER =====
def random_delay(min_sec=5, max_sec=15):
    """Delay random yang lebih natural"""
    delay = random.uniform(min_sec, max_sec)
    return delay

def human_typing(element, text):
    """Simulasi typing seperti manusia"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))  # Delay antar karakter

# ===== SETUP EDGE =====
print("Memulai Edge browser...")
options = Options()

options.add_argument("user-data-dir=C:\\Users\\krido\\AppData\\Local\\Microsoft\\Edge\\User Data")
options.add_argument("profile-directory=Profile 17")

# Hilangkan deteksi automation
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")

service = Service(EDGE_DRIVER_PATH)
driver = webdriver.Edge(service=service, options=options)

# Hapus properti webdriver
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

wait = WebDriverWait(driver, 10)

# Buka mesin pencari
driver.get(SEARCH_URL)
print(f"Browser terbuka di {SEARCH_URL}\n")

# ===== PENCARIAN DENGAN BATAS =====
MAX_SEARCHES = 30  # Batasi jumlah pencarian
search_count = 0
used_keywords = []  # Track keyword yang sudah dipakai

try:
    while search_count < MAX_SEARCHES:
        # Pilih keyword yang belum dipakai
        available_keywords = [k for k in keywords if k not in used_keywords]
        
        if not available_keywords:
            print("Semua keyword sudah digunakan.")
            break
            
        keyword = random.choice(available_keywords)
        used_keywords.append(keyword)
        
        try:
            # Tunggu delay random sebelum search
            delay = random_delay(8, 20)
            print(f"Menunggu {delay:.1f} detik sebelum pencarian berikutnya...")
            time.sleep(delay)
            
            # Cari search box
            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # Clear dengan cara natural
            search_box.clear()
            time.sleep(random.uniform(0.5, 1.5))
            
            # Ketik dengan simulasi human typing
            human_typing(search_box, keyword)
            time.sleep(random.uniform(0.5, 1.0))
            search_box.send_keys(Keys.ENTER)
            
            search_count += 1
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{current_time}] Search #{search_count}/{MAX_SEARCHES}: {keyword}")
            
            # Simulasi baca hasil (scroll random)
            time.sleep(random.uniform(2, 5))
            
            # Random scroll untuk simulasi membaca
            scroll_amount = random.randint(200, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1, 3))
            
            # Kadang klik hasil pencarian (30% chance)
            if random.random() < 0.3:
                try:
                    results = driver.find_elements(By.CSS_SELECTOR, "h2 a")
                    if results:
                        result_to_click = random.choice(results[:5])  # Klik salah satu dari 5 hasil teratas
                        print(f"  → Membuka hasil pencarian...")
                        result_to_click.click()
                        time.sleep(random.uniform(5, 10))  # Baca halaman
                        driver.back()  # Kembali ke hasil
                        time.sleep(random.uniform(2, 4))
                except:
                    pass
            
            # Kembali ke halaman utama untuk search berikutnya
            driver.get(SEARCH_URL)
            time.sleep(random.uniform(2, 4))
            
        except Exception as e:
            print(f"Error saat search: {e}")
            print("Mencoba kembali ke halaman utama...")
            driver.get(SEARCH_URL)
            time.sleep(3)
            continue

    print(f"\n{'='*50}")
    print(f"Selesai! Total pencarian: {search_count}")
    print(f"{'='*50}")

except KeyboardInterrupt:
    print(f"\n\n{'='*50}")
    print("Script dihentikan manual")
    print(f"Total pencarian yang dilakukan: {search_count}")
    print(f"{'='*50}")

except Exception as e:
    print(f"\nError tidak terduga: {e}")

finally:
    print("\nMenutup browser dalam 5 detik...")
    time.sleep(5)
    driver.quit()
    print("Selesai!")