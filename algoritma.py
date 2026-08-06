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
        if data[i - 1] == 0:
            # harga sebelumnya 0 (delisting/data korup) - pembagian tak
            # terdefinisi, lewati transisi ini alih-alih crash.
            continue
        r = ((data[i] - data[i - 1]) / data[i - 1]) * 100
        hasil.append(r)

    return hasil