nilai = int(input("masukan nilai:"))
if nilai >= 90:
    print("A - Luar biasa")
elif nilai >= 80:
    print("B - Bagus")
elif nilai >= 70:
    print("C - Cukup")
elif nilai >= 60:
    print("D - Perlu belajar lebih")
else:
    print("F - Gagal")
print(f"Nilai kamu: {nilai}")