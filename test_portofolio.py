import portofolio
from portofolio import analisis_saham, ambil_data_harga, susun_laporan


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
    cache_tanggal = {"BBCA": "2026-08-05"}

    hasil = ambil_data_harga(["BBCA", "BBRI"], cache, cache_tanggal, live=False)

    assert hasil == {"BBCA": {"harga": [9800.0, 9900.0], "tanggal_terakhir": "2026-08-05"}}


def test_ambil_data_harga_live_berhasil(monkeypatch):
    data_live = {"harga": [100.0, 200.0], "tanggal_terakhir": "2026-08-06"}
    monkeypatch.setattr(portofolio, "ambil_harga_online", lambda ticker: data_live)

    hasil = ambil_data_harga(["BBCA"], {}, {}, live=True)

    assert hasil == {"BBCA": data_live}


def test_ambil_data_harga_live_gagal_fallback_ke_cache(monkeypatch, capsys):
    monkeypatch.setattr(portofolio, "ambil_harga_online", lambda ticker: None)

    cache = {"BBCA": [9800.0, 9900.0]}
    cache_tanggal = {"BBCA": "2026-08-04"}
    hasil = ambil_data_harga(["BBCA"], cache, cache_tanggal, live=True)

    assert hasil == {"BBCA": {"harga": [9800.0, 9900.0], "tanggal_terakhir": "2026-08-04"}}
    assert "PERINGATAN" in capsys.readouterr().out


def test_ambil_data_harga_live_gagal_tanpa_cache(monkeypatch):
    monkeypatch.setattr(portofolio, "ambil_harga_online", lambda ticker: None)

    hasil = ambil_data_harga(["TLKM"], {}, {}, live=True)

    assert hasil == {}


def _hasil_saham(tanggal, pl=100000):
    return {
        "tanggal_terakhir": tanggal,
        "harga_terakhir": 6500.0,
        "return_harian": 1.0,
        "nilai_pasar": 6500000,
        "modal": 6400000,
        "pl": pl,
        "pl_persen": 1.56,
    }


def test_susun_laporan_menandai_total_saat_tanggal_campuran():
    laporan = [
        ("BBCA", _hasil_saham("2026-08-06")),
        ("BBRI", _hasil_saham("2026-08-04")),
    ]

    teks = susun_laporan(laporan, total_nilai=13000000, total_modal=12800000)

    assert "TOTAL*" in teks
    assert "PERINGATAN: TOTAL*" in teks
    assert "2026-08-04" in teks and "2026-08-06" in teks


def test_susun_laporan_tidak_menandai_saat_tanggal_sama():
    laporan = [
        ("BBCA", _hasil_saham("2026-08-06")),
        ("BBRI", _hasil_saham("2026-08-06")),
    ]

    teks = susun_laporan(laporan, total_nilai=13000000, total_modal=12800000)

    assert "TOTAL*" not in teks
    assert "PERINGATAN" not in teks
