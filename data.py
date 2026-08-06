def baca_semua_harga(nama_file):
    try:
        hasil = {}

        with open(nama_file, "r") as file:
            for i, baris in enumerate(file):
                if i == 0:
                    continue

                bagian = baris.strip().split(",")
                ticker = bagian[0]
                harga = float(bagian[2])

                if ticker not in hasil:
                    hasil[ticker] = []
                hasil[ticker].append(harga)

        return hasil
    except FileNotFoundError:
        print(f"PERINGATAN: file {nama_file} tidak ditemukan")
        return None


def baca_tanggal_terakhir(nama_file):
    try:
        hasil = {}

        with open(nama_file, "r") as file:
            for i, baris in enumerate(file):
                if i == 0:
                    continue

                bagian = baris.strip().split(",")
                ticker = bagian[0]
                tanggal = bagian[1]

                hasil[ticker] = tanggal

        return hasil
    except FileNotFoundError:
        print(f"PERINGATAN: file {nama_file} tidak ditemukan")
        return None


def tulis_posisi(nama_file, data_posisi):
    with open(nama_file, "w") as file:
        file.write("ticker,lot,harga_beli\n")
        for tkr, info in data_posisi.items():
            file.write(f"{tkr},{info['lot']},{info['harga_beli']}\n")


def tambah_posisi(nama_file, ticker, lot, harga_beli):
    posisi = baca_posisi(nama_file)
    if posisi is None:
        return False

    if ticker in posisi:
        lot_lama = posisi[ticker]["lot"]
        harga_lama = posisi[ticker]["harga_beli"]
        lot_baru = lot_lama + lot
        harga_baru = round((lot_lama * harga_lama + lot * harga_beli) / lot_baru)
        posisi[ticker] = {"lot": lot_baru, "harga_beli": harga_baru}
    else:
        posisi[ticker] = {"lot": lot, "harga_beli": harga_beli}

    tulis_posisi(nama_file, posisi)
    return True


def hapus_posisi(nama_file, ticker):
    posisi = baca_posisi(nama_file)
    if posisi is None:
        return False

    if ticker not in posisi:
        print(f"PERINGATAN: posisi {ticker} tidak ditemukan")
        return False

    del posisi[ticker]
    tulis_posisi(nama_file, posisi)
    return True


def baca_posisi(nama_file):
    try:
        hasil = {}

        with open(nama_file, "r") as file:
            for i, baris in enumerate(file):
                if i == 0:
                    continue

                bagian = baris.strip().split(",")

                ticker = bagian[0]
                lot = int(bagian[1])
                harga_beli = int(bagian[2])

                hasil[ticker] = {
                    "lot": lot,
                    "harga_beli": harga_beli,
                }

        return hasil
    except FileNotFoundError:
        print(f"PERINGATAN: file {nama_file} tidak ditemukan")
        return None