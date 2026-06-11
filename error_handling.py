try:
    angka = int(input("Masukkan angka: "))
    hasil = 100 / angka
    print(f"Hasil: {hasil}")
except ValueError:
    print("Error: Input harus berupa angka.")
except ZeroDivisionError:
    print("Error: Tidak bisa membagi dengan nol.")
else:
    print("Program berjalan tanpa error.")