import sqlite3
import kisiler_islemleri as kisiler

try:
    # Veritabanı bağlantısını oluştur
    conn = sqlite3.connect("database.db")
    print("veri tabanına başarıyla bağlanıldı")
    # Bir cursor (imleç) oluştur
    cursor = conn.cursor()
    
    # Örnek bir tablo oluştur
    cursor.execute("""CREATE TABLE IF NOT EXISTS kisiler(
                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      ad_soyad TEXT NOT NULL,
                      eposta TEXT NOT NULL, 
                      telefon TEXT NOT NULL, 
                      unvan TEXT, 
                      aciklama TEXT, 
                      birim_id INTEGER)""")
    print("Tablo başarıyla oluşturuldu.")
    
    while True:
        print("\nne yapacaksınız ?")
        print("1.kişi ekle")
        print("2.kişi sil")
        print("3.kişi bul")
        print("4.kişi güncelle")
        print("5.Rehberi indir")
        print("6.Filtrele")
        print("7.Genel Arama")
        print("8.çıkış")
        
        secim = input("seçiminiz:")
        if secim == "1":
            kisiler.kisi_ekle(cursor, conn)
        elif secim == "2":
            kisiler.kisi_sil(cursor, conn)
        elif secim == "3":
            kisiler.kisi_bul(cursor)
        elif secim == "4":
            kisiler.kisi_guncelle(cursor, conn)
        elif secim == "5":
            kisiler.rehber_indir(cursor)
        elif secim == "6":
            kisiler.kisileri_filtrele(cursor)
        elif secim == "7":
            kisiler.genel_arama(cursor)
        elif secim == "8":
            print("çıkış yapılıyor")
            break
        else:
            print("geçersiz seçim yaptınız, lütfen tekrar deneyin")
                
    
    # Değişiklikleri kaydet
    conn.commit()
    
    # Var olan tabloları listele
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("veri tabanındaki tablolar:", tables) 
    
    # verileri okuma(ekstra)
    cursor.execute("SELECT * FROM kisiler")
    rows = cursor.fetchall()
    for now in rows:
        print(rows)
    
except sqlite3.Error as e:
    print(f"Hata: {e}")

finally:
    if conn:
        conn.close()