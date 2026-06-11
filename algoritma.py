def cari_terbesar(data):
    if not data:
        return None
    terbesar = data[0]
    for nilai in data:
        if nilai > terbesar:
            terbesar = nilai
    return terbesar
def hitung_rata_rata(data):
    if not data:
        return None
    return sum(data) / len(data)
def cari_terkecil(data):
    if not data:
        return None
    terkecil = data[0]
    for nilai in data:
        if nilai < terkecil:
            terkecil = nilai
    return terkecil
def hitung_return_harian(data):
    hasil = []

    for i in range(1, len(data)):
        r = ((data[i] - data[i - 1]) / data[i - 1]) * 100
        hasil.append(r)

    return hasil

if __name__ == "__main__":
    hasil = hitung_return_harian([100, 102, 99, 105])

    assert round(hasil[0], 2) == 2.00
    assert round(hasil[1], 2) == -2.94
    assert round(hasil[2], 2) == 6.06

    assert cari_terkecil([5]) == 5
    assert cari_terkecil([-2, -8, -1]) == -8
    assert cari_terkecil([]) is None

    assert cari_terbesar([-2, -8, -1]) == -1

    assert hitung_rata_rata([2, 4]) == 3.0

    print("Semua tes berhasil")