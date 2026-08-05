from data import baca_semua_harga, baca_posisi


def test_baca_semua_harga():
    hasil = baca_semua_harga("harga.csv")
    assert hasil == {
        "BBCA": [9800.0, 9850.0, 9700.0, 9900.0],
        "BBRI": [4500.0, 4480.0, 4550.0, 4600.0],
        "BMRI": [6100.0, 6150.0, 6050.0, 6200.0],
    }


def test_baca_semua_harga_file_tidak_ada():
    assert baca_semua_harga("tidak_ada.csv") is None


def test_baca_posisi():
    hasil = baca_posisi("posisi.csv")
    assert hasil == {
        "BBCA": {"lot": 10, "harga_beli": 9500},
        "BBRI": {"lot": 50, "harga_beli": 4400},
        "BMRI": {"lot": 20, "harga_beli": 6300},
    }


def test_baca_posisi_file_tidak_ada():
    assert baca_posisi("tidak_ada.csv") is None
