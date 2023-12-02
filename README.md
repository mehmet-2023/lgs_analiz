# Ders Düzenleme Programı

Bu program, öğrencilerin ders deneme sonuçlarını kaydetmelerine, analiz etmelerine ve yapay zeka kullanarak öneriler alabilmelerine olanak tanıyan bir araçtır.

## Gereksinimler

- Python 3.x
- [Matplotlib](https://matplotlib.org/stable/users/installing.html)
- [OpenAI GPT-3.5-turbo API Key](https://beta.openai.com/signup/)
- Tkinter (Bu genellikle Python ile birlikte gelir)

## Kurulum

1. Python'u [Python Resmi Web Sitesi'nden](https://www.python.org/) indirip kurun.
2. Proje dizinine gidin ve terminal veya komut istemcisine şu komutu girin:

    ```bash
    pip install matplotlib openai
    ```
## Kullanım

1. Menüdeki seçenekleri takip ederek veri ekleyebilir, getirebilir, grafikleri görebilir ve yapay zeka analizi yapabilirsiniz.

2. **Veri Ekleme:**
    - Öğrenci adı, tarih, dersler ve konular için yanlış sayılar gibi verileri ekleyebilirsiniz.

3. **Veri Getirme:**
    - Eklenmiş verileri öğrenci adına göre listeleyebilirsiniz.

4. **Grafikler:**
    - Deneme numarasına göre toplam yanlış sayısı çizgi grafiği.
    - Derslere göre yanlış dağılımı sütun grafiği.
    - Konulara göre yanlış dağılımı sütun grafiği.

5. **Yapay Zeka Analizi:**
    - Öğrencinin yanlış yaptığı konulara göre OpenAI GPT-3.5-turbo modeli ile analiz yapabilirsiniz.

## API Key

Program, OpenAI GPT-3.5-turbo modelini kullanarak yapay zeka analizi yapabilmek için bir API anahtarına ihtiyaç duyar. Bu anahtarı `api_key` değişkenine ekleyin.

## Lisans

Bu program açık kaynaklıdır ve [MIT Lisansı](LICENSE) altında lisanslanmıştır.
