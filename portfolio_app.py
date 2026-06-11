def load_data():
    portofolio = {}
    try:
        with open("portfolio.txt", "r") as f:
            for baris in f:
                data = baris.strip().split(",")
                kode = data[0]
                harga = int(data[1])
                lembar = int(data[2])
                portofolio[kode] = {"harga": harga, "lembar": lembar}
    except FileNotFoundError:
        pass
    return portofolio
def save_data(portofolio):
    with open("portfolio.txt", "w") as f:
        for kode, data in portofolio.items():
            f.write(f"{kode},{data['harga']},{data['lembar']}\n")
def tampilkan(portofolio):
    if len(portofolio) == 0:
        print("Portfolio kosong.")
        return
    
    print("\n=== PORTFOLIO KAMU ===")
    total = 0
    for kode, data in portofolio.items():
        modal = data["harga"] * data["lembar"]
        total += modal
        print(f"{kode} | Harga: {data['harga']:,} | Lembar: {data['lembar']} | Modal: Rp {modal:,}")
    print(f"{'='*30}")
    print(f"Total Modal: Rp {total:,}")
def tambah_saham(portofolio):
    kode = input("kode Saham(contoh: BBCA): ").upper()
    try:
        harga = int(input("Harga beli: "))
        lembar = int(input("Jumlah lembar: "))
        portofolio[kode] = {"harga": harga, "lembar": lembar}
        save_data(portofolio)
        print(f"{kode} berhasil ditambahkan.")
    except ValueError:
        print("Input tidak valid. Pastikan harga dan jumlah lembar adalah angka.")
def hapus_saham(portofolio):
    kode = input("Masukkan kode saham yang ingin dihapus: ").upper()
    if kode in portofolio:
        del portofolio[kode]
        save_data(portofolio)
        print(f"{kode} berhasil dihapus.")
    else:
        print(f"{kode} tidak ditemukan dalam portfolio.")
def main():
    portofolio = load_data()
    
    while True:
        print("\n=== PORTFOLIO TRACKER ===")
        print("1. Tampilkan Portfolio")
        print("2. Tambah Saham")
        print("3. Hapus Saham")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ")
        
        if pilihan == "1":
            tampilkan(portofolio)
        elif pilihan == "2":
            tambah_saham(portofolio)
        elif pilihan == "3":
            hapus_saham(portofolio)
        elif pilihan == "4":
            print("Terima kasih telah menggunakan Portfolio Tracker!")
            break
        else:
            print("Opsi tidak valid. Silakan pilih antara 1-4.")

main()