import sqlite3
import csv
import re


def baglanti_kur():
    return sqlite3.connect("database.db")

# E-posta doğrulama
import re

def eposta_dogrula(eposta):
    # Basit e-posta doğrulama
    eposta_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(eposta_regex, eposta) is not None

def ad_soyad_dogrula(ad_soyad):
    # Ad Soyad sadece harfler ve boşluk içerebilir
    return ad_soyad.replace(" ", "").isalpha()



def kisi_ekle(cursor, conn):
    while True:
        ad_soyad = input("Ad Soyad: ").strip()
        if ad_soyad.lower() == 'q':  # Çıkış seçeneği
            print("Ekleme işlemi iptal edildi.")
            return
        if not ad_soyad_dogrula(ad_soyad):
            print("Ad Soyad yalnızca harflerden oluşmalı! Lütfen tekrar deneyin.")
        else:
            break

    # E-posta doğrulama
    while True:
        eposta = input("Eposta (Çıkmak için 'q' yazın): ").strip()
        if eposta.lower() == 'q':
            print("Ekleme işlemi iptal edildi.")
            return
        if not eposta_dogrula(eposta):
            print("Geçersiz e-posta adresi! Lütfen tekrar deneyin.")
        else:
            break

    telefon = input("Telefon: ").strip()
    unvan = input("Unvan (isteğe bağlı): ").strip()
    aciklama = input("Açıklama (isteğe bağlı): ").strip()
    birim_id = input("Birim ID (isteğe bağlı): ").strip()

    cursor.execute("""INSERT INTO kisiler (ad_soyad, eposta, telefon, unvan, aciklama, birim_id)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   (ad_soyad, eposta, telefon, unvan or None, aciklama or None, birim_id or None))
    conn.commit()
    print(f"{ad_soyad} başarıyla tabloya eklendi!")



    
def kisi_sil(cursor, conn):
    sil_id = input("Silmek istediğiniz kişinin ID'sini girin: ")
    cursor.execute("DELETE FROM kisiler WHERE id=?", (sil_id,))
    conn.commit()
    print(f"{sil_id} ID'li kişi başarıyla silindi!")

    
def kisi_bul(cursor):
    aranan = input("Aramak istediğiniz kişinin adını veya soyadını girin: ")
    cursor.execute("SELECT * FROM kisiler WHERE ad_soyad LIKE ?", (f"%{aranan}%",))
    rows = cursor.fetchall()

    if rows:
        print("Arama sonuçları:")
        for row in rows:
            print(row)
    else:
        print("Hiçbir sonuç bulunamadı.")

    
def kisi_guncelle(cursor, conn):
    guncellenecek_id = input("Güncellemek istediğiniz kişinin ID'sini girin: ").strip()
    cursor.execute("SELECT * FROM kisiler WHERE id=?", (guncellenecek_id,))
    kisi = cursor.fetchone()

    if not kisi:
        print("Belirtilen ID'ye sahip kişi bulunamadı.")
        return

    print(f"Mevcut bilgiler: {kisi}")
    while True:
        guncel_ad_soyad = input(f"Ad Soyad ({kisi[1]}): ").strip() or kisi[1]
        if guncel_ad_soyad.lower() == 'q':  # Çıkış seçeneği
            print("Güncelleme işlemi iptal edildi.")
            return
        if not ad_soyad_dogrula(guncel_ad_soyad):
            print("Ad Soyad yalnızca harflerden oluşmalı! Lütfen tekrar deneyin.")
        else:
            break

    while True:
        guncel_eposta = input(f"Eposta ({kisi[2]}) (Çıkmak için 'q' yazın): ").strip() or kisi[2]
        if guncel_eposta.lower() == 'q':
            print("Güncelleme işlemi iptal edildi.")
            return
        if not eposta_dogrula(guncel_eposta):
            print("Geçersiz e-posta adresi! Lütfen tekrar deneyin.")
        else:
            break

    guncel_telefon = input(f"Telefon ({kisi[3]}): ").strip() or kisi[3]
    guncel_unvan = input(f"Unvan ({kisi[4]}): ").strip() or kisi[4]
    guncel_aciklama = input(f"Açıklama ({kisi[5]}): ").strip() or kisi[5]
    guncel_birim_id = input(f"Birim ID ({kisi[6]}): ").strip() or kisi[6]

    cursor.execute("""UPDATE kisiler SET ad_soyad=?, eposta=?, telefon=?, unvan=?, aciklama=?, birim_id=?
                      WHERE id=?""",
                   (guncel_ad_soyad, guncel_eposta, guncel_telefon, guncel_unvan, guncel_aciklama, guncel_birim_id, guncellenecek_id))
    conn.commit()
    print(f"{guncellenecek_id} ID'li kişi başarıyla güncellendi!")


from openpyxl import Workbook

from openpyxl import Workbook

def rehber_indir(cursor):
    # Veritabanındaki tüm kayıtları al
    cursor.execute("SELECT * FROM kisiler")
    rows = cursor.fetchall()

    if not rows:
        print("Rehber boş, indirilecek veri yok.")
        return

    # Kullanıcıdan dosya adı al
    while True:
        dosya_adi = input("Rehber dosyanızın adını giriniz (varsayılan: rehber.xlsx): ").strip()
        if not dosya_adi:  # Varsayılan ad kullan
            dosya_adi = "rehber.xlsx"
        elif not dosya_adi.endswith(".xlsx"):
            dosya_adi += ".xlsx"

        # Geçerli bir dosya adı olduğundan emin olun
        if "/" in dosya_adi or "\\" in dosya_adi or ":" in dosya_adi or "*" in dosya_adi:
            print("Geçersiz dosya adı, lütfen tekrar deneyin.")
        else:
            break

    # Excel dosyası oluştur ve veri ekle
    wb = Workbook()
    ws = wb.active
    ws.title = "Rehber"

    # Başlık satırını ekle
    ws.append(["ID", "Ad Soyad", "Eposta", "Telefon", "Unvan", "Açıklama", "Birim ID"])

    # Kayıtları ekle
    for row in rows:
        ws.append(row)

    # Excel dosyasını kaydet
    wb.save(dosya_adi)
    print(f"Rehber başarıyla '{dosya_adi}' olarak kaydedildi.")



def kisileri_filtrele(cursor):
    print("Filtreleme kriterleri:")
    print("1. Ad Soyad")
    print("2. E-posta")
    print("3. Telefon")
    print("4. Ünvan")
    print("5. Açıklama")
    print("6. Birim ID")
    
    secim = input("filtreleme ayarını seçiniz(1-6):")
    
    filtre_kriterleri = {
        "1": "ad_soyad",
        "2": "eposta",
        "3": "telefon",
        "4": "unvan",
        "5": "aciklama",
        "6": "birim_id"
    }
    alan = filtre_kriterleri.get(secim)
    if not alan:
        print("geçersiz seçim")
        return
    
    deger = input(f"{alan.replace('_', ' ').title()} için filtre değeri girin: ")
    
    if alan == "birim_id":  # Birim ID tam eşleşme ister
        cursor.execute(f"SELECT * FROM kisiler WHERE {alan}=?", (deger,))
    else:  # Diğerleri LIKE ile kısmi eşleşme sağlar
        cursor.execute(f"SELECT * FROM kisiler WHERE {alan} LIKE ?", (f"%{deger}%",))
    
    rows = cursor.fetchall()
    if rows:
        print("Filtreleme sonuçları:")
        for row in rows:
            print(row)
    else:
        print("Sonuç bulunamadı.")

def genel_arama(cursor):
    arama_terimi = input("Aramak istediğiniz terimi girin: ")

    query = """
    SELECT * FROM kisiler
    WHERE ad_soyad LIKE ?
    OR eposta LIKE ?
    OR telefon LIKE ?
    OR unvan LIKE ?
    OR aciklama LIKE ?
    OR CAST(birim_id AS TEXT) LIKE ?
    """
    cursor.execute(query, (f"%{arama_terimi}%", f"%{arama_terimi}%", f"%{arama_terimi}%",
                           f"%{arama_terimi}%", f"%{arama_terimi}%", f"%{arama_terimi}%"))

    rows = cursor.fetchall()

    # Sonuçları göster
    if rows:
        print("Arama sonuçları:")
        for row in rows:
            print(row)
    else:
        print("Sonuç bulunamadı.")