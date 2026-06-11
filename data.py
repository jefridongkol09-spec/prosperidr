def baca_harga(nama_file):
    try:
        hasil = []

        with open(nama_file, "r") as file:
            for i, baris in enumerate(file):
                if i == 0:
                    continue

                bagian = baris.strip().split(",")

                harga = float(bagian[1])

                hasil.append(harga)

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
if __name__ == "__main__":
    hasil_harga = baca_harga("harga_bbca.csv")

    assert hasil_harga == [9800, 9850, 9700, 9900]

    hasil_posisi = baca_posisi("posisi.csv")

    assert hasil_posisi == {
        "BBCA": {"lot": 10, "harga_beli": 9500},
        "BBRI": {"lot": 50, "harga_beli": 4400},
        "BMRI": {"lot": 20, "harga_beli": 6300},
    }

    print("Semua tes berhasil!")