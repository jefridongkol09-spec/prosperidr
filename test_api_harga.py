import pandas as pd

import api_harga


class FakeTicker:
    def __init__(self, riwayat):
        self._riwayat = riwayat

    def history(self, period):
        return self._riwayat


def test_ambil_harga_online_berhasil(monkeypatch):
    simbol_dipakai = []

    def fake_ticker(simbol):
        simbol_dipakai.append(simbol)
        return FakeTicker(pd.DataFrame({"Close": [100.123, 200.456]}))

    monkeypatch.setattr(api_harga.yf, "Ticker", fake_ticker)

    hasil = api_harga.ambil_harga_online("BBCA")

    assert hasil == [100.12, 200.46]
    assert simbol_dipakai == ["BBCA.JK"]


def test_ambil_harga_online_hari_terakhir_belum_tersedia(monkeypatch):
    # Hari terakhir kadang NaN (closing price belum dilaporkan Yahoo Finance)
    # tanpa DataFrame-nya kosong - harus dibuang, bukan ikut jadi "nan" di list.
    df = pd.DataFrame({"Close": [100.0, 200.0, float("nan")]})
    monkeypatch.setattr(api_harga.yf, "Ticker", lambda simbol: FakeTicker(df))

    assert api_harga.ambil_harga_online("BBCA") == [100.0, 200.0]


def test_ambil_harga_online_semua_nan(monkeypatch):
    df = pd.DataFrame({"Close": [float("nan"), float("nan")]})
    monkeypatch.setattr(api_harga.yf, "Ticker", lambda simbol: FakeTicker(df))

    assert api_harga.ambil_harga_online("BBCA") is None


def test_ambil_harga_online_kosong(monkeypatch):
    monkeypatch.setattr(
        api_harga.yf, "Ticker", lambda simbol: FakeTicker(pd.DataFrame({"Close": []}))
    )

    assert api_harga.ambil_harga_online("TIDAKADA") is None


def test_ambil_harga_online_error_jaringan(monkeypatch):
    def gagal(simbol):
        raise ConnectionError("network down")

    monkeypatch.setattr(api_harga.yf, "Ticker", gagal)

    assert api_harga.ambil_harga_online("BBCA") is None
