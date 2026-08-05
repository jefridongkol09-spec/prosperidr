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