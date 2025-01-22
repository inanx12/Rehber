from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import csv

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Flash mesajları için gerekli

# Veritabanı bağlantısı
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Anasayfa
@app.route("/")
def index():
    return render_template("index.html")

# Kişileri Listele
@app.route("/kisilerim")
def kisiler():
    query = request.args.get("q", "").strip()  # Arama sorgusu
    filter_field = request.args.get("filter_field", "").strip()  # Filtreleme alanı
    conn = get_db_connection()

    if query:  # Eğer arama sorgusu varsa
        if filter_field:  # Belirli bir alanda arama yapılacaksa
            sql_query = f"SELECT * FROM kisiler WHERE {filter_field} LIKE ?"
            kisiler = conn.execute(sql_query, (f"%{query}%",)).fetchall()
        else:  # Genel arama yapılacaksa
            sql_query = """
                SELECT * FROM kisiler WHERE 
                ad_soyad LIKE ? OR 
                eposta LIKE ? OR 
                telefon LIKE ? OR 
                unvan LIKE ? OR 
                birim_id LIKE ?
            """
            kisiler = conn.execute(sql_query, (f"%{query}%",) * 5).fetchall()
    else:  # Hiçbir arama yapılmamışsa tüm kişileri listele
        kisiler = conn.execute("SELECT * FROM kisiler").fetchall()

    conn.close()
    return render_template("kisiler.html", kisiler=kisiler, query=query, filter_field=filter_field)

# Kişi Ekleme
@app.route("/kisi_ekle", methods=["GET", "POST"])
def kisi_ekle():
    if request.method == "POST":
        ad_soyad = request.form.get("ad_soyad")
        eposta = request.form.get("eposta")
        telefon = request.form.get("telefon")
        unvan = request.form.get("unvan")
        aciklama = request.form.get("aciklama")
        birim_id = request.form.get("birim_id")

        if not ad_soyad or not eposta or not telefon:
            flash("Lütfen tüm zorunlu alanları doldurun!", "danger")
            return redirect(url_for("kisi_ekle"))

        conn = get_db_connection()
        conn.execute("""INSERT INTO kisiler (ad_soyad, eposta, telefon, unvan, aciklama, birim_id)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                     (ad_soyad, eposta, telefon, unvan, aciklama, birim_id))
        conn.commit()
        conn.close()
        flash("Kişi başarıyla eklendi!", "success")
        return redirect(url_for("kisiler"))
    return render_template("kisi_ekle.html")

# Kişi Güncelleme
@app.route("/kisi_guncelle/<int:id>", methods=["GET", "POST"])
def kisi_guncelle(id):
    conn = get_db_connection()
    kisi = conn.execute("SELECT * FROM kisiler WHERE id = ?", (id,)).fetchone()

    if not kisi:
        flash("Kişi bulunamadı!", "danger")
        return redirect(url_for("kisiler"))

    if request.method == "POST":
        ad_soyad = request.form.get("ad_soyad")
        eposta = request.form.get("eposta")
        telefon = request.form.get("telefon")
        unvan = request.form.get("unvan")
        aciklama = request.form.get("aciklama")
        birim_id = request.form.get("birim_id")

        if not ad_soyad or not eposta or not telefon:
            flash("Lütfen tüm zorunlu alanları doldurun!", "danger")
            return redirect(url_for("kisi_guncelle", id=id))

        conn.execute("""UPDATE kisiler
                        SET ad_soyad = ?, eposta = ?, telefon = ?, unvan = ?, aciklama = ?, birim_id = ?
                        WHERE id = ?""",
                     (ad_soyad, eposta, telefon, unvan, aciklama, birim_id, id))
        conn.commit()
        conn.close()
        flash("Kişi başarıyla güncellendi!", "success")
        return redirect(url_for("kisiler"))

    conn.close()
    return render_template("kisi_guncelle.html", kisi=kisi)

# Rehberi İndir
@app.route("/rehberi_indir")
def indir():
    conn = get_db_connection()
    kisiler = conn.execute("SELECT * FROM kisiler").fetchall()
    conn.close()

    with open("rehber.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["ID", "Ad Soyad", "Eposta", "Telefon", "Unvan", "Açıklama", "Birim ID"])
        for kisi in kisiler:
            csvwriter.writerow([kisi["id"], kisi["ad_soyad"], kisi["eposta"], kisi["telefon"],
                                kisi["unvan"], kisi["aciklama"], kisi["birim_id"]])

    return send_file("rehber.csv", as_attachment=True, download_name="rehber.csv")

@app.route('/kisi_sil/<int:id>', methods=['POST'])
def kisi_sil(id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kisiler WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        flash("Kişi başarıyla silindi!", "success")
    except Exception as e:
        flash(f"Bir hata oluştu: {e}", "danger")
    return redirect('/kisiler')




if __name__ == "__main__":
    app.run(debug=True)
