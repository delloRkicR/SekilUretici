import math
import tkinter as tk
from tkinter import messagebox

MAX_KENAR = 10_000_000
MIN_ZOOM = 0.2
MAX_ZOOM = 40


def noktali(sayi):
    return f"{sayi:,}".replace(",", ".")


class CokgenUygulamasi:
    def __init__(self, root):
        self.root = root
        self.n = 6
        self.zoom = 1.0
        self.ox = 0
        self.oy = 0
        self.son_nokta = None
        self.pencereyi_kur()
        self.olaylari_bagla()
        self.giris_degisti()

    def pencereyi_kur(self):
        self.root.title("Çokgen Çizici")
        self.root.geometry("500x600")
        self.root.minsize(320, 400)

        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        self.sekil = self.canvas.create_polygon(0, 0, 0, 0, 0, 0,
                                                fill="#8ecae6", outline="#023047", width=2)

        self.bilgi = tk.Label(self.root, font=("Segoe UI", 11))
        self.bilgi.pack(pady=(6, 0))

        self.uyari = tk.Label(self.root, height=1, fg="#c1121f", font=("Segoe UI", 10))
        self.uyari.pack()

        ipucu = "Tekerlek: yakınlaştır   Sürükle: kaydır   Çift tık: sıfırla"
        tk.Label(self.root, text=ipucu, fg="gray", font=("Segoe UI", 9)).pack()

        alt = tk.Frame(self.root)
        alt.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(alt, text="Kenar sayısı:", font=("Segoe UI", 11)).pack(side=tk.LEFT)

        self.deger = tk.StringVar(value=str(self.n))
        self.giris = tk.Entry(alt, textvariable=self.deger, width=14,
                              justify="center", font=("Segoe UI", 12))
        self.giris.pack(side=tk.LEFT, padx=8)
        self.giris.focus_set()

        tk.Button(alt, text="Çiz", width=8, command=self.butona_basildi).pack(side=tk.LEFT)

    def olaylari_bagla(self):
        self.deger.trace_add("write", lambda *_: self.giris_degisti())
        self.root.bind("<Return>", lambda e: self.butona_basildi())
        self.canvas.bind("<Configure>", lambda e: self.ciz())
        self.canvas.bind("<MouseWheel>", self.tekerlek)
        self.canvas.bind("<Button-4>", self.tekerlek)
        self.canvas.bind("<Button-5>", self.tekerlek)
        self.canvas.bind("<ButtonPress-1>", self.surukle_basla)
        self.canvas.bind("<B1-Motion>", self.surukle)
        self.canvas.bind("<Double-Button-1>", self.sifirla)

    def oku(self):
        metin = self.deger.get().strip()
        if not metin:
            raise ValueError("Bir sayı girin.")
        if metin.startswith("-") and metin[1:].isdecimal():
            raise ValueError("Negatif sayı olmaz.")
        if not metin.isdecimal():
            raise ValueError("Sadece pozitif tam sayı girin.")
        sayi = metin.lstrip("0")
        if len(sayi) > 8 or int(sayi or 0) > MAX_KENAR:
            raise ValueError(f"En fazla {noktali(MAX_KENAR)} kenar girilebilir.")
        n = int(sayi or 0)
        if n < 3:
            raise ValueError("En az 3 kenar gerekli.")
        return n

    def giris_degisti(self):
        try:
            self.n = self.oku()
        except ValueError as hata:
            self.uyari.config(text=str(hata))
            return False
        self.uyari.config(text="")
        self.ciz()
        return True

    def butona_basildi(self):
        if not self.giris_degisti():
            messagebox.showwarning("Uyarı", self.uyari.cget("text"))

    def merkez(self):
        cx = self.canvas.winfo_width() / 2 + self.ox
        cy = self.canvas.winfo_height() / 2 + self.oy
        return cx, cy

    def temel_yaricap(self):
        kisa = min(self.canvas.winfo_width(), self.canvas.winfo_height())
        return max(kisa / 2 - 15, 10)

    def cizilecek_kenar(self, r):
        sinir = max(360, int(math.pi * math.sqrt(r / 0.25)))
        return min(self.n, sinir)

    def ciz(self):
        if self.canvas.winfo_width() < 20 or self.canvas.winfo_height() < 20:
            return
        cx, cy = self.merkez()
        r = self.temel_yaricap() * self.zoom
        k = self.cizilecek_kenar(r)
        adim = 2 * math.pi / k
        noktalar = []
        for i in range(k):
            a = i * adim - math.pi / 2
            noktalar.append(cx + r * math.cos(a))
            noktalar.append(cy + r * math.sin(a))
        self.canvas.coords(self.sekil, *noktalar)
        self.canvas.itemconfigure(self.sekil, width=2 if self.n <= 100 else 1)
        self.bilgi_yaz()

    def bilgi_yaz(self):
        yuzde = round(self.zoom * 100)
        self.bilgi.config(text=f"{noktali(self.n)} kenarlı çokgen  |  yakınlaştırma %{yuzde}")

    def tekerlek(self, event):
        yukari = event.num == 4 or event.delta > 0
        self.yaklastir(1.1 if yukari else 1 / 1.1, event.x, event.y)

    def yaklastir(self, carpan, mx, my):
        yeni = min(MAX_ZOOM, max(MIN_ZOOM, self.zoom * carpan))
        oran = yeni / self.zoom
        cx, cy = self.merkez()
        self.ox += (mx - cx) * (1 - oran)
        self.oy += (my - cy) * (1 - oran)
        self.zoom = yeni
        self.ciz()

    def surukle_basla(self, event):
        self.son_nokta = (event.x, event.y)

    def surukle(self, event):
        if self.son_nokta is None:
            return
        dx = event.x - self.son_nokta[0]
        dy = event.y - self.son_nokta[1]
        self.ox += dx
        self.oy += dy
        self.son_nokta = (event.x, event.y)
        self.canvas.move(self.sekil, dx, dy)

    def sifirla(self, event=None):
        self.zoom = 1.0
        self.ox = 0
        self.oy = 0
        self.ciz()


if __name__ == "__main__":
    root = tk.Tk()
    CokgenUygulamasi(root)
    root.mainloop()