import time
import random
import os
import shutil
import subprocess
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# ===== KONFIGURASI =====
EDGE_DRIVER_PATH = "./driver/stable/150.0.4078.83/msedgedriver.exe"
SEARCH_URL = "https://www.bing.com"

# Folder profile Edge ASLI (jangan diubah)
ORIGINAL_USER_DATA_DIR = r"C:\Users\krido\AppData\Local\Microsoft\Edge\User Data"

# Folder tempat menyimpan COPY profile (aman dipakai Selenium, tidak konflik dgn Edge biasa)
SELENIUM_USER_DATA_DIR = r"C:\SeleniumProfiles\EdgeUserData"

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

def close_running_edge():
    """Pastikan tidak ada proses Edge yang masih berjalan (mencegah error DevToolsActivePort)"""
    print("Memastikan tidak ada proses Edge yang berjalan...")
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "msedge.exe", "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        subprocess.run(
            ["taskkill", "/F", "/IM", "msedgedriver.exe", "/T"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)
        print("✓ Proses Edge lama sudah ditutup (jika ada)")
    except Exception as e:
        print(f"Peringatan saat menutup Edge: {e}")

def ensure_profile_copied(profile_name):
    """
    Copy folder profile dari Edge asli ke folder Selenium khusus.
    Hanya di-copy jika belum ada, supaya tidak menimpa data setiap run
    dan supaya login/cookies tetap terbawa.

    Jika folder asli tidak ditemukan (path salah / profile belum pernah
    dibuat di Edge asli), fungsi ini TIDAK akan crash. Ia akan membiarkan
    Edge membuat profile baru yang kosong di lokasi Selenium, dan
    memberi peringatan bahwa user perlu login manual nanti.

    Return: (dst_profile_path, is_fresh_profile)
    """
    src_profile_path = os.path.join(ORIGINAL_USER_DATA_DIR, profile_name)
    dst_profile_path = os.path.join(SELENIUM_USER_DATA_DIR, profile_name)

    # Copy juga "Local State" (berisi info enkripsi/daftar profil) jika belum ada
    src_local_state = os.path.join(ORIGINAL_USER_DATA_DIR, "Local State")
    dst_local_state = os.path.join(SELENIUM_USER_DATA_DIR, "Local State")

    os.makedirs(SELENIUM_USER_DATA_DIR, exist_ok=True)

    if not os.path.exists(dst_local_state) and os.path.exists(src_local_state):
        print("Menyalin 'Local State'...")
        shutil.copy2(src_local_state, dst_local_state)

    # Sudah pernah di-copy sebelumnya -> pakai yang ada
    if os.path.exists(dst_profile_path):
        print(f"✓ Profile '{profile_name}' sudah pernah disalin sebelumnya, lewati proses copy")
        return dst_profile_path, False

    # Folder asli tidak ditemukan -> jangan crash, buat profile baru kosong
    if not os.path.exists(src_profile_path):
        print(f"⚠ PERINGATAN: Folder profile asli tidak ditemukan di:")
        print(f"  {src_profile_path}")
        print(f"  Kemungkinan penyebab: path ORIGINAL_USER_DATA_DIR salah, atau")
        print(f"  profile '{profile_name}' belum pernah dibuat/dipakai di Edge asli.")
        print(f"  Script akan tetap lanjut dengan profile BARU (kosong, belum login).")
        print(f"  Kamu perlu login manual ke Microsoft/Bing saat browser terbuka nanti.\n")
        # Tidak perlu copytree apapun; Edge otomatis membuat folder profile
        # baru saat pertama kali dijalankan dengan profile-directory ini.
        return dst_profile_path, True

    # Folder asli ada -> copy seperti biasa
    print(f"Menyalin profile '{profile_name}' ke lokasi Selenium (sekali saja, mohon tunggu)...")
    shutil.copytree(src_profile_path, dst_profile_path)
    print(f"✓ Profile '{profile_name}' berhasil disalin ke {dst_profile_path}")
    return dst_profile_path, False

def create_driver(profile_name):
    """Membuat driver Edge dengan profil (copy) tertentu"""
    print(f"\n{'='*60}")
    print(f"Memulai Edge browser dengan {profile_name}...")
    print(f"{'='*60}")

    # Pastikan profile sudah di-copy ke folder aman
    _, is_fresh_profile = ensure_profile_copied(profile_name)

    options = Options()
    options.add_argument(f"user-data-dir={SELENIUM_USER_DATA_DIR}")
    options.add_argument(f"profile-directory={profile_name}")

    # Hilangkan deteksi automation
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--remote-debugging-port=0")  # biarkan OS pilih port bebas

    service = Service(EDGE_DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)

    # Hapus properti webdriver
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    if is_fresh_profile:
        print(f"{'!'*60}")
        print(f"Profile ini BARU/KOSONG (belum ada data login).")
        print(f"Silakan login manual ke akun Microsoft di jendela browser")
        print(f"yang baru terbuka. Script akan menunggu 45 detik sebelum")
        print(f"mulai melakukan pencarian.")
        print(f"{'!'*60}")
        driver.get("https://login.live.com")
        time.sleep(45)

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

                # Sesekali (setelah 5-7 search) beri jeda panjang seolah user lagi ngobrol/baca lain
                if search_count > 0 and search_count % random.randint(5, 7) == 0:
                    long_break = random.uniform(30, 90)
                    print(f"⏸  Jeda panjang {long_break:.1f} detik (simulasi user sedang idle)...")
                    time.sleep(long_break)
                else:
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

                # Simulasi baca hasil awal
                time.sleep(random.uniform(2, 5))

                # Scroll bertahap (2-3 kali) untuk simulasi membaca, bukan satu scroll besar
                scroll_steps = random.randint(2, 3)
                for _ in range(scroll_steps):
                    scroll_amount = random.randint(150, 500)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    time.sleep(random.uniform(0.8, 2.5))

                # Kadang klik hasil pencarian (30% chance)
                if random.random() < 0.3:
                    try:
                        results = driver.find_elements(By.CSS_SELECTOR, "h2 a")
                        if results:
                            result_to_click = random.choice(results[:5])
                            print(f"  → Membuka hasil pencarian...")
                            result_to_click.click()
                            # Waktu baca artikel lebih variatif, kadang lama
                            read_time = random.uniform(5, 15) if random.random() < 0.7 else random.uniform(15, 35)
                            time.sleep(read_time)
                            driver.back()
                            time.sleep(random.uniform(2, 4))
                    except:
                        pass

                # Kembali ke halaman utama untuk search berikutnya
                driver.get(SEARCH_URL)
                time.sleep(random.uniform(2, 5))

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

    # Pastikan Edge yang sedang berjalan ditutup dulu agar tidak konflik
    close_running_edge()

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