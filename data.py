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
if __name__ == "__main__":
    hasil_semua = baca_semua_harga("harga.csv")

    assert hasil_semua == {
        "BBCA": [9800.0, 9850.0, 9700.0, 9900.0],
        "BBRI": [4500.0, 4480.0, 4550.0, 4600.0],
        "BMRI": [6100.0, 6150.0, 6050.0, 6200.0],
    }

    hasil_posisi = baca_posisi("posisi.csv")

    assert hasil_posisi == {
        "BBCA": {"lot": 10, "harga_beli": 9500},
        "BBRI": {"lot": 50, "harga_beli": 4400},
        "BMRI": {"lot": 20, "harga_beli": 6300},
    }

    print("Semua tes berhasil!")