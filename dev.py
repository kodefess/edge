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
EDGE_DRIVER_PATH = "./driver/145.0.3800.65/msedgedriver.exe"
SEARCH_URL = "https://www.bing.com"

# ===== LIST PROFIL =====
# Tambah atau kurangi profil sesuai kebutuhan
PROFILES = [
    "Profile 2",
    "Profile 3",
    "Profile 4",
    "Profile 5",
    "Profile 6",
    "Profile 7",
    "Profile 8",
    "Profile 9",
    "Profile 10",
]

# Jumlah pencarian per profil
SEARCHES_PER_PROFILE = 30

# Keyword yang lebih natural dan variatif (topik berbeda)
keywords = [
    "beginner guide to stock market investing",
    "most in demand programming languages for the future",
    "easy healthy breakfast ideas for busy mornings",
    "recent trends in technology and innovation",
    "python data analysis tutorial for beginners",
    "best budget laptops under 1000 dollars",
    "practical ways to improve workplace productivity",
    "top travel destinations in southeast asia",
    "machine learning project ideas for beginners",
    "effective home workout routines without equipment",
    "digital marketing strategies for small businesses",
    "recommended books to read this year",
    "practical solutions to reduce climate change impact",
    "step by step guide to starting a podcast",
    "basic photography tips for beginners",
    "comparison of popular web development frameworks",
    "personal financial planning tips for beginners",
    "meditation techniques to reduce stress and anxiety",
    "simple sustainable living ideas for everyday life",
    "career development tips for long term growth"
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
        time.sleep(random.uniform(0.05, 0.2))

def create_driver(profile_name):
    """Membuat driver Edge dengan profil tertentu"""
    print(f"\n{'='*60}")
    print(f"Memulai Edge browser dengan {profile_name}...")
    print(f"{'='*60}")
    
    options = Options()
    options.add_argument("user-data-dir=C:\\Users\\krido\\AppData\\Local\\Microsoft\\Edge\\User Data")
    options.add_argument(f"profile-directory={profile_name}")
    
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
    
    return driver

def run_searches_for_profile(driver, profile_name, max_searches=SEARCHES_PER_PROFILE):
    """Menjalankan pencarian untuk satu profil"""
    wait = WebDriverWait(driver, 10)
    
    driver.get(SEARCH_URL)
    print(f"Browser terbuka di {SEARCH_URL}")
    print(f"Target: {max_searches} pencarian untuk {profile_name}\n")
    
    search_count = 0
    used_keywords = []
    
    try:
        while search_count < max_searches:
            available_keywords = [k for k in keywords if k not in used_keywords]
            
            if not available_keywords:
                print("Semua keyword sudah digunakan, mereset keyword pool...")
                used_keywords = []
                available_keywords = keywords
                
            keyword = random.choice(available_keywords)
            used_keywords.append(keyword)
            
            try:
                delay = random_delay(8, 20)
                print(f"Menunggu {delay:.1f} detik sebelum pencarian berikutnya...")
                time.sleep(delay)
                
                search_box = wait.until(
                    EC.presence_of_element_located((By.NAME, "q"))
                )
                
                search_box.clear()
                time.sleep(random.uniform(0.5, 1.5))
                
                human_typing(search_box, keyword)
                time.sleep(random.uniform(0.5, 1.0))
                search_box.send_keys(Keys.ENTER)
                
                search_count += 1
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{current_time}] [{profile_name}] Search #{search_count}/{max_searches}: {keyword}")
                
                time.sleep(random.uniform(2, 5))
                
                scroll_amount = random.randint(200, 800)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(1, 3))
                
                # Kadang klik hasil pencarian (30% chance)
                if random.random() < 0.3:
                    try:
                        results = driver.find_elements(By.CSS_SELECTOR, "h2 a")
                        if results:
                            result_to_click = random.choice(results[:5])
                            print(f"  → Membuka hasil pencarian...")
                            result_to_click.click()
                            time.sleep(random.uniform(5, 10))
                            driver.back()
                            time.sleep(random.uniform(2, 4))
                    except:
                        pass
                
                driver.get(SEARCH_URL)
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error saat search: {e}")
                print("Mencoba kembali ke halaman utama...")
                driver.get(SEARCH_URL)
                time.sleep(3)
                continue
        
        print(f"\n{'='*60}")
        print(f"✓ Selesai untuk {profile_name}! Total pencarian: {search_count}")
        print(f"{'='*60}")
        return search_count
        
    except KeyboardInterrupt:
        print(f"\n\n{'='*60}")
        print(f"Script dihentikan manual untuk {profile_name}")
        print(f"Total pencarian yang dilakukan: {search_count}")
        print(f"{'='*60}")
        return search_count
        
    except Exception as e:
        print(f"\nError tidak terduga pada {profile_name}: {e}")
        return search_count

# ===== MAIN PROGRAM =====
def main():
    total_profiles = len(PROFILES)
    total_searches_all = 0
    
    print("\n" + "="*60)
    print("MULAI AUTOMATED SEARCH - MULTIPLE PROFILES")
    print("="*60)
    print(f"Total profil          : {total_profiles}")
    print(f"Target per profil     : {SEARCHES_PER_PROFILE} pencarian")
    print(f"Total target pencarian: {total_profiles * SEARCHES_PER_PROFILE}")
    print("="*60)
    print("Daftar profil yang akan dijalankan:")
    for i, p in enumerate(PROFILES, 1):
        print(f"  {i:>2}. {p}")
    print("="*60)
    
    for idx, profile in enumerate(PROFILES, 1):
        print(f"\n\n{'#'*60}")
        print(f"PROFIL {idx}/{total_profiles}: {profile}")
        print(f"{'#'*60}")
        
        driver = None
        try:
            driver = create_driver(profile)
            searches_done = run_searches_for_profile(driver, profile, max_searches=SEARCHES_PER_PROFILE)
            total_searches_all += searches_done
            
        except Exception as e:
            print(f"\n✗ Error pada {profile}: {e}")
            
        finally:
            if driver:
                print(f"\nMenutup browser untuk {profile}...")
                time.sleep(3)
                driver.quit()
                print(f"✓ Browser {profile} ditutup")
        
        # Delay antar profil (kecuali profil terakhir)
        if idx < total_profiles:
            delay_between_profiles = random.uniform(10, 20)
            print(f"\n⏳ Menunggu {delay_between_profiles:.1f} detik sebelum membuka profil berikutnya...")
            print(f"   Profil berikutnya: {PROFILES[idx]}")
            time.sleep(delay_between_profiles)
    
    # Summary akhir
    print("\n\n" + "="*60)
    print("SEMUA PROFIL SELESAI!")
    print("="*60)
    print(f"Total profil diproses : {total_profiles}")
    print(f"Total pencarian       : {total_searches_all}")
    print(f"Rata-rata per profil  : {total_searches_all/total_profiles:.1f}")
    print("="*60)
    print("\nScript selesai!")

if __name__ == "__main__":
    main()
