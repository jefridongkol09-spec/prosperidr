with open("data.txt", "w") as f:
    f.write("BBCA,9200,100\n")
    f.write("BBRI,4500,200\n")
    f.write("BMRI,6700,150\n")

print("File berhasil ditulis")

# BACA dari file
with open("data.txt", "r") as f:
    isi = f.read()
    print(isi)
with open("data.txt", "r") as f:
    for baris in f:
        data = baris.strip().split(",")
        kode = data[0]
        harga = int(data[1])
        lembar = int(data[2])
        modal = harga * lembar
        print(f"{kode} | Modal: Rp {modal:,}")