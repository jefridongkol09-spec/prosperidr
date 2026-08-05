from portofolio import analisis_saham


def test_analisis_saham():
    hasil = analisis_saham([9800.0, 9850.0, 9700.0, 9900.0], 10, 9500)
    assert round(hasil["pl"], 0) == 400000
