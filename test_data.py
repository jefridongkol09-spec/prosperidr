from data import (
    baca_semua_harga,
    baca_posisi,
    baca_tanggal_terakhir,
    tambah_posisi,
    hapus_posisi,
)


def test_baca_semua_harga():
    hasil = baca_semua_harga("harga.csv")
    assert hasil == {
        "BBCA": [9800.0, 9850.0, 9700.0, 9900.0],
        "BBRI": [4500.0, 4480.0, 4550.0, 4600.0],
        "BMRI": [6100.0, 6150.0, 6050.0, 6200.0],
    }


def test_baca_semua_harga_file_tidak_ada():
    assert baca_semua_harga("tidak_ada.csv") is None


def test_baca_tanggal_terakhir():
    hasil = baca_tanggal_terakhir("harga.csv")
    assert hasil == {
        "BBCA": "2025-01-04",
        "BBRI": "2025-01-04",
        "BMRI": "2025-01-04",
    }


def test_baca_tanggal_terakhir_file_tidak_ada():
    assert baca_tanggal_terakhir("tidak_ada.csv") is None


def test_baca_posisi():
    hasil = baca_posisi("posisi.csv")
    assert hasil == {
        "BBCA": {"lot": 10, "harga_beli": 9500},
        "BBRI": {"lot": 50, "harga_beli": 4400},
        "BMRI": {"lot": 20, "harga_beli": 6300},
    }


def test_baca_posisi_file_tidak_ada():
    assert baca_posisi("tidak_ada.csv") is None


def test_tambah_posisi_ticker_baru(tmp_path):
    file_path = tmp_path / "posisi.csv"
    file_path.write_text("ticker,lot,harga_beli\nBBCA,10,9500\n")

    berhasil = tambah_posisi(str(file_path), "BBRI", 20, 4500)

    assert berhasil is True
    assert baca_posisi(str(file_path)) == {
        "BBCA": {"lot": 10, "harga_beli": 9500},
        "BBRI": {"lot": 20, "harga_beli": 4500},
    }


def test_tambah_posisi_gabung_ticker_sama(tmp_path):
    # rata-rata berbobot: (10*9500 + 10*9700) / 20 = 9600
    file_path = tmp_path / "posisi.csv"
    file_path.write_text("ticker,lot,harga_beli\nBBCA,10,9500\n")

    berhasil = tambah_posisi(str(file_path), "BBCA", 10, 9700)

    assert berhasil is True
    assert baca_posisi(str(file_path)) == {
        "BBCA": {"lot": 20, "harga_beli": 9600},
    }


def test_tambah_posisi_file_tidak_ada(tmp_path):
    file_path = tmp_path / "tidak_ada.csv"
    assert tambah_posisi(str(file_path), "BBCA", 10, 9500) is False


def test_hapus_posisi_ticker_ada(tmp_path):
    file_path = tmp_path / "posisi.csv"
    file_path.write_text("ticker,lot,harga_beli\nBBCA,10,9500\nBBRI,50,4400\n")

    berhasil = hapus_posisi(str(file_path), "BBCA")

    assert berhasil is True
    assert baca_posisi(str(file_path)) == {
        "BBRI": {"lot": 50, "harga_beli": 4400},
    }


def test_hapus_posisi_ticker_tidak_ada(tmp_path):
    file_path = tmp_path / "posisi.csv"
    file_path.write_text("ticker,lot,harga_beli\nBBCA,10,9500\n")

    berhasil = hapus_posisi(str(file_path), "TLKM")

    assert berhasil is False
    assert baca_posisi(str(file_path)) == {
        "BBCA": {"lot": 10, "harga_beli": 9500},
    }


def test_hapus_posisi_file_tidak_ada(tmp_path):
    file_path = tmp_path / "tidak_ada.csv"
    assert hapus_posisi(str(file_path), "BBCA") is False
