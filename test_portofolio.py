import portofolio
from portofolio import analisis_saham, ambil_data_harga


def test_analisis_saham():
    hasil = analisis_saham([9800.0, 9850.0, 9700.0, 9900.0], 10, 9500)
    assert round(hasil["pl"], 0) == 400000


def test_analisis_saham_return_harian_pakai_dua_hari_terakhir():
    # [100, 110, 105]: hari terakhir turun dari 110 ke 105 = -4.55%.
    # Bug lama menghitung elemen pertama vs terakhir dari seluruh window
    # (105 vs 100 = +5.00%), bukan hari terakhir vs hari sebelumnya.
    hasil = analisis_saham([100.0, 110.0, 105.0], 1, 100)
    assert round(hasil["return_harian"], 2) == -4.55


def test_ambil_data_harga_tanpa_live_pakai_cache():
    cache = {"BBCA": [9800.0, 9900.0]}
    hasil = ambil_data_harga(["BBCA", "BBRI"], cache, live=False)
    assert hasil == {"BBCA": [9800.0, 9900.0]}


def test_ambil_data_harga_live_berhasil(monkeypatch):
    monkeypatch.setattr(portofolio, "ambil_harga_online", lambda ticker: [100.0, 200.0])

    hasil = ambil_data_harga(["BBCA"], {}, live=True)

    assert hasil == {"BBCA": [100.0, 200.0]}


def test_ambil_data_harga_live_gagal_fallback_ke_cache(monkeypatch, capsys):
    monkeypatch.setattr(portofolio, "ambil_harga_online", lambda ticker: None)

    cache = {"BBCA": [9800.0, 9900.0]}
    hasil = ambil_data_harga(["BBCA"], cache, live=True)

    assert hasil == {"BBCA": [9800.0, 9900.0]}
    assert "PERINGATAN" in capsys.readouterr().out


def test_ambil_data_harga_live_gagal_tanpa_cache(monkeypatch):
    monkeypatch.setattr(portofolio, "ambil_harga_online", lambda ticker: None)

    hasil = ambil_data_harga(["TLKM"], {}, live=True)

    assert hasil == {}
