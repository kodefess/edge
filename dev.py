import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime

# ===== KONFIGURASI =====
SEARCH_URL = "https://www.bing.com"

# List profil yang akan digunakan secara berurutan
PROFILES = [
    "Profile 2",
]

# Keyword yang lebih natural dan variatif
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
    delay = random.uniform(min_sec, max_sec)
    return delay

def human_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))

def create_driver(profile_name):
    print(f"\n{'='*60}")
    print(f"Memulai Edge browser dengan {profile_name}...")
    print(f"{'='*60}")
    
    options = Options()
    options.add_argument(r"user-data-dir=C:\Users\krido\AppData\Local\Microsoft\Edge\User Data")
    options.add_argument(f"profile-directory={profile_name}")
    
    # Anti automation detection
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    
    # ✅ webdriver-manager dipakai di sini
    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    
    return driver

def run_searches_for_profile(driver, profile_name, max_searches=30):
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
                used_keywords = []
                available_keywords = keywords
                
            keyword = random.choice(available_keywords)
            used_keywords.append(keyword)
            
            try:
                delay = random_delay(8, 20)
                print(f"Menunggu {delay:.1f} detik...")
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
                print(f"[{current_time}] [{profile_name}] #{search_count}: {keyword}")
                
                time.sleep(random.uniform(2, 5))
                driver.execute_script(
                    f"window.scrollBy(0, {random.randint(200, 800)});"
                )
                
                if random.random() < 0.3:
                    results = driver.find_elements(By.CSS_SELECTOR, "h2 a")
                    if results:
                        random.choice(results[:5]).click()
                        time.sleep(random.uniform(5, 10))
                        driver.back()
                
                driver.get(SEARCH_URL)
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"Error search: {e}")
                driver.get(SEARCH_URL)
                time.sleep(3)
        
        print(f"\n✓ Selesai {profile_name}, total: {search_count}")
        return search_count
        
    except KeyboardInterrupt:
        print(f"\nScript dihentikan manual ({profile_name})")
        return search_count

# ===== MAIN =====
def main():
    total_searches_all = 0
    
    print("="*60)
    print("MULAI AUTOMATED SEARCH")
    print("="*60)
    
    for profile in PROFILES:
        driver = None
        try:
            driver = create_driver(profile)
            total_searches_all += run_searches_for_profile(driver, profile, 30)
        finally:
            if driver:
                time.sleep(3)
                driver.quit()
    
    print("\nSEMUA SELESAI")
    print(f"Total pencarian: {total_searches_all}")

if __name__ == "__main__":
    main()
