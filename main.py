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
EDGE_DRIVER_PATH = "./driver/stable/144.0.3719.115/msedgedriver.exe"
SEARCH_URL = "https://www.bing.com"

# List profil yang akan digunakan secara berurutan
PROFILES = [
    "Profile 16",
]

# Keyword yang lebih natural dan variatif (topik berbeda)
keywords = [
    "beginner running tips to improve stamina fast",
    "home workout routines without gym equipment",
    "morning habits that boost energy all day",
    "healthy snack ideas for late night cravings",
    "simple mental health practices for busy adults",
    "best football drills to practice alone",
    "how to stay consistent with a fitness routine",
    "easy meal prep ideas for a busy work week",
    "daily skincare routine for oily and acne prone skin",
    "budget travel tips for first time solo travelers",
    "how to save money without feeling restricted",
    "best productivity apps to organize your life",
    "weekend activities to reset your mind and body",
    "how to reduce screen time without deleting social media",
    "simple mindfulness exercises for stress relief",
    "tips to improve focus while working from home",
    "how to build healthy sleep habits naturally",
    "outdoor hobbies that are good for mental health",
    "ways to stay motivated when goals feel overwhelming",
    "easy lifestyle changes for a healthier life"
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

def run_searches_for_profile(driver, profile_name, max_searches=30):
    """Menjalankan pencarian untuk satu profil"""
    wait = WebDriverWait(driver, 10)
    
    # Buka mesin pencari
    driver.get(SEARCH_URL)
    print(f"Browser terbuka di {SEARCH_URL}")
    print(f"Target: {max_searches} pencarian untuk {profile_name}\n")
    
    search_count = 0
    used_keywords = []
    
    try:
        while search_count < max_searches:
            # Pilih keyword yang belum dipakai
            available_keywords = [k for k in keywords if k not in used_keywords]
            
            if not available_keywords:
                print("Semua keyword sudah digunakan, mereset keyword pool...")
                used_keywords = []
                available_keywords = keywords
                
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
                print(f"[{current_time}] [{profile_name}] Search #{search_count}/{max_searches}: {keyword}")
                
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
                            result_to_click = random.choice(results[:5])
                            print(f"  → Membuka hasil pencarian...")
                            result_to_click.click()
                            time.sleep(random.uniform(5, 10))
                            driver.back()
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
    print(f"Total profil: {total_profiles}")
    print(f"Target per profil: 30 pencarian")
    print(f"Total target pencarian: {total_profiles * 30}")
    print("="*60)
    
    for idx, profile in enumerate(PROFILES, 1):
        print(f"\n\n{'#'*60}")
        print(f"PROFIL {idx}/{total_profiles}: {profile}")
        print(f"{'#'*60}")
        
        driver = None
        try:
            # Buat driver untuk profil ini
            driver = create_driver(profile)
            
            # Jalankan pencarian
            searches_done = run_searches_for_profile(driver, profile, max_searches=30)
            total_searches_all += searches_done
            
        except Exception as e:
            print(f"\n✗ Error pada {profile}: {e}")
            
        finally:
            if driver:
                print(f"\nMenutup browser untuk {profile}...")
                time.sleep(3)
                driver.quit()
                print(f"✓ Browser {profile} ditutup")
        
        # Delay sebelum membuka profil berikutnya (kecuali profil terakhir)
        if idx < total_profiles:
            delay_between_profiles = random.uniform(10, 20)
            print(f"\n⏳ Menunggu {delay_between_profiles:.1f} detik sebelum membuka profil berikutnya...")
            time.sleep(delay_between_profiles)
    
    # Summary
    print("\n\n" + "="*60)
    print("SEMUA PROFIL SELESAI!")
    print("="*60)
    print(f"Total profil diproses: {total_profiles}")
    print(f"Total pencarian dilakukan: {total_searches_all}")
    print(f"Rata-rata per profil: {total_searches_all/total_profiles:.1f}")
    print("="*60)
    print("\nScript selesai!")

if __name__ == "__main__":
    main()