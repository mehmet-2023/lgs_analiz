import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict
import operator
import openai
from tkinter import messagebox

# Veritabanı bağlantısını oluştur
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
api_key = "API KEY"
# Dersler tablosunu oluştur
cursor.execute('''CREATE TABLE IF NOT EXISTS dersler (
                    ogrenci_ad TEXT,
                    ders_ad TEXT,
                    konu TEXT,
                    tarih DATE,
                    deneme INTEGER,
                    yanlis INTEGER,
                    bolum TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tablo_adı (
                    id INTEGER PRIMARY KEY,
                    deneme_no INTEGER
                )''')

cursor.execute("SELECT * FROM dersler")
veriler = cursor.fetchall()

def main_menu():
    print("DERS DÜZENLEME PROGRAMI")
    print("1. Veri Ekle")
    print("2. Veri Getir")
    print("3. Deneme Numarasına Göre Çizgi Grafiği Göster (Toplam Yanlış Sayı)")
    print("4. Derslere Göre Yanlış Dağılımı Sütun Grafiği Göster")
    print("5. Konulara Göre Yanlış Dağılımı Sütun Grafiği Göster")
    print("6. Sonuçlarını Yapay Zeka İle Analiz Et")
    print("0. Çıkış")


def ders_ekle(ogrenci_ad, ders_ad, konu, tarih, deneme, yanlis, bolum):
    cursor.execute(
        "INSERT INTO dersler (ogrenci_ad, ders_ad, konu, tarih, deneme, yanlis, bolum) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (ogrenci_ad, ders_ad, konu, tarih, deneme, yanlis, bolum))
    connection.commit()


def get_deneme_data(ogrenci_ad, ders_ad):
    cursor.execute("SELECT deneme, SUM(yanlis) FROM dersler WHERE ogrenci_ad=? AND ders_ad=? GROUP BY deneme",
                   (ogrenci_ad, ders_ad))
    return cursor.fetchall()


def get_ders_yanlis_data(ogrenci_ad, ders_ad):
    cursor.execute("SELECT ders_ad, SUM(yanlis) FROM dersler WHERE ogrenci_ad=? GROUP BY ders_ad", (ogrenci_ad,))
    return cursor.fetchall()


def get_konu_yanlis_data(ogrenci_ad, ders_ad):
    cursor.execute("SELECT konu, SUM(yanlis) FROM dersler WHERE ogrenci_ad=? AND ders_ad=? GROUP BY konu",
                   (ogrenci_ad, ders_ad))
    return cursor.fetchall()


def veri_ekle():
    ogrenci_ad = input("Öğrenci Adı: ")
    tarih = input("Tarih: ")
    dersler = ["Türkçe", "İnkılap Tarihi", "Din Kültürü", "İngilizce", "Matematik", "Fen Bilimleri"]
    ders_konulari = defaultdict(list)
    cursor.execute("SELECT deneme_no FROM tablo_adı WHERE rowid=1")  
    deneme_no = cursor.fetchone()
    if deneme_no is None:
        deneme_no = 1  
        cursor.execute("UPDATE tablo_adı SET deneme_no = ? WHERE rowid=1", (deneme_no,))
        connection.commit()  
    else:
        deneme_no = deneme_no[0]  
    for ders in dersler:
        yanlis_sayisi = int(input(f"{ders} için yanlış sayısı: "))
        konular = []
        for i in range(yanlis_sayisi):
            konu = input(f"{i+1}. Soruda yanlış yapılan konu: ")
            konular.append(konu)
        ders_konulari[ders] = konular

    for ders, konular in ders_konulari.items():
        for konu in konular:
            ders_ekle(ogrenci_ad, ders, konu, tarih, deneme_no, 1, "Bölüm")
    cursor.execute("INSERT INTO tablo_adı (deneme_no) VALUES (?)", (deneme_no+1,))
    connection.commit()
    print("Veri başarıyla eklendi.")

def dersleri_getir(ogrenci_ad):
    cursor.execute("SELECT * FROM dersler WHERE ogrenci_ad=?", (ogrenci_ad,))
    return cursor.fetchall()

def veri_getir():
    ogrenci_ad = input("Öğrenci Adı Girin: ")
    derslerim = dersleri_getir(ogrenci_ad)

    if not derslerim:
        print("Alınacak Veri Yok")
        return

    for ders in derslerim:
        print("Öğrenci Adı:", ders[0])
        print("Ders Adı:", ders[1])
        print("Konu:", ders[2])
        print("Tarih:", ders[3])
        print("Deneme:", ders[4])
        print("Yanlış Sayısı:", ders[5])
        print("-------------")


def deneme_numarasina_gore_cizgi_grafigi_goster():
    ogrenci_ad = input("Öğrenci Adı Girin: ")
    deneme_data = defaultdict(int)
    dersler = ["Türkçe", "İnkılap Tarihi", "Din Kültürü", "İngilizce", "Matematik", "Fen Bilimleri"]
    for ders in dersler:
        deneme_yanlis_data = get_deneme_data(ogrenci_ad, ders)
        for deneme, yanlis in deneme_yanlis_data:
            deneme_data[deneme] += yanlis

    if not deneme_data:
        print("Alınacak Veri Yok")
        return

    denemeler = list(deneme_data.keys())
    yanlislar = list(deneme_data.values())

    plt.figure(figsize=(10, 6))
    plt.plot(denemeler, yanlislar, marker='o')
    plt.xlabel("Deneme Numarası")
    plt.ylabel("Toplam Yanlış Sayısı")
    plt.title(f"{ogrenci_ad} İsimli Öğrencinin Tüm Derslerde Deneme Numarasına Göre Toplam Yanlış Sayıları")
    plt.tight_layout()
    plt.show()


def derslere_gore_yanlis_dagilimi_cizgi_grafigi_goster():
    ogrenci_ad = input("Öğrenci Adı Girin: ")
    ders_yanlis_data = get_ders_yanlis_data(ogrenci_ad, "Toplam")

    if not ders_yanlis_data:
        print("Alınacak Veri Yok")
        return

    dersler, yanlislar = zip(*ders_yanlis_data)

    plt.figure(figsize=(10, 6))
    plt.bar(dersler, yanlislar)  # Sütun grafiği için plt.bar kullanılıyor
    plt.xlabel("Ders")
    plt.ylabel("Toplam Yanlış Sayısı")
    plt.title(f"{ogrenci_ad} İsimli Öğrencinin Derslere Göre Toplam Yanlış Dağılımı")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def konulara_gore_yanlis_dagilimi_sutun_grafigi_goster():
    ogrenci_ad = input("Öğrenci Adı Girin: ")
    konu_yanlis_data = defaultdict(int)
    dersler = ["Türkçe", "İnkılap Tarihi", "Din Kültürü", "İngilizce", "Matematik", "Fen Bilimleri"]
    for ders in dersler:
        konu_data = get_konu_yanlis_data(ogrenci_ad, ders)
        for konu, yanlis in konu_data:
            konu_yanlis_data[konu] += yanlis

    if not konu_yanlis_data:
        print("Alınacak Veri Yok")
        return

    sorted_konu_yanlis_data = dict(sorted(konu_yanlis_data.items(), key=operator.itemgetter(1), reverse=True))
    konular = list(sorted_konu_yanlis_data.keys())
    yanlislar = list(sorted_konu_yanlis_data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(konular, yanlislar)
    plt.xlabel("Konu")
    plt.ylabel("Toplam Yanlış Sayısı")
    plt.title(f"{ogrenci_ad} İsimli Öğrencinin Tüm Derslerde Konulara Göre En Çok Yanlış Yapılan Konular")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def yapay_zeka(veriler):
    sonuclar = [] 

    for veri in veriler:
        ogrenci_ad, ders_ad, konu, tarih, deneme, yanlis, bolum = veri
        sonuc = f"{ogrenci_ad} isimli öğrenci, {ders_ad} dersinde {konu} konusunda {yanlis} yanlış yapmış."
        sonuclar.append(sonuc)
    return sonuclar
def analiz_et():
        messagebox.showinfo(title="Lütfen Bekleyin",message="Bu uzun sürebilir. Programı terk etmeyin")
        x = yapay_zeka(veriler)
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "user", "content": "Merhaba, ben bir 8. sınıf öğrencisiyim ve ders deneme sonuçlarımı analiz etmek istiyorum aşağıda yanlış yaptığım konular var. Bana örnek soru, LGS'ye göre nerelere çalışmalıyım söyler misin, sorular zor olsun. Yanlış yaptığım konular burada."+str(x)},
                 ],
                api_key=api_key
            )
        print(response["choices"][0]["message"]["content"] + "\n")
def ana_program():
    while True:
        main_menu()
        secim = input("Seçiminizi Girin: ")
        if secim == "1":
            veri_ekle()
        elif secim == "2":
            veri_getir()
        elif secim == "3":
            deneme_numarasina_gore_cizgi_grafigi_goster()
        elif secim == "4":
            derslere_gore_yanlis_dagilimi_cizgi_grafigi_goster()
        elif secim == "5":
            konulara_gore_yanlis_dagilimi_sutun_grafigi_goster()
        elif secim == "6":
            analiz_et()
        elif secim == "0":
            connection.close()
            print("Programdan çıkılıyor.")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    ana_program()
