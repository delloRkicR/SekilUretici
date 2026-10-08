# Çokgen Çizici

Girdiğiniz kenar sayısına göre düzgün çokgen çizen, yakınlaştırıp kaydırabildiğiniz hafif bir masaüstü uygulaması. Sadece Python ile gelen `tkinter` kullanır, ek kütüphane gerekmez.

## Özellikler

- 3 ile 10.000.000 arasında istediğiniz kenar sayısı
- Siz yazarken anlık çizim
- Fare tekerleğiyle imlecin olduğu noktaya yakınlaştırma (%20 - %4000)
- Sürükleyerek kaydırma
- Çift tıkla görünümü sıfırlama
- Çok büyük kenar sayılarında bile akıcı çalışır
- Hatalı girişte anlaşılır uyarı mesajı

## Kurulum

Python 3.x gerekli. Windows ve macOS için Python ile birlikte `tkinter` de gelir. Linux'ta gerekirse şunu kurun:

    sudo apt install python3-tk

`cokgen.py` dosyasını indirin, başka bir şey kurmanız gerekmez.

## Kullanım

    python cokgen.py

| İşlem | Nasıl |
| --- | --- |
| Kenar sayısını değiştirme | Alttaki kutuya yazın, çokgen anında güncellenir |
| Yakınlaştırma / uzaklaştırma | Fare tekerleği |
| Kaydırma | Farenin sol tuşuyla sürükleyin |
| Görünümü sıfırlama | Çizim alanına çift tıklayın |

## Nasıl çalışır?

Kenar sayısı çok büyüdüğünde çokgen zaten bir daireden ayırt edilemez. Bu yüzden uygulama, ekranda farkı görünmeyecek kenar sayısından fazlasını çizmez. Bilgi satırında her zaman girdiğiniz gerçek kenar sayısı görünür.

## Katkı

Hata bulursanız Issue açabilir, düzeltme veya yeni özellik için Pull Request gönderebilirsiniz.

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile paylaşılmıştır.
