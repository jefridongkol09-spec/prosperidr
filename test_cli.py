import subprocess
import sys
from pathlib import Path

import pytest

from portofolio import main

PATH_PORTOFOLIO_PY = Path(__file__).parent / "portofolio.py"


def test_laporan_berjalan(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "posisi.csv").write_text("ticker,lot,harga_beli\nBBCA,10,9500\n")
    (tmp_path / "harga.csv").write_text(
        "ticker,tanggal,close\n"
        "BBCA,2025-01-01,9800\n"
        "BBCA,2025-01-02,9900\n"
    )

    main(["laporan"])

    assert "BBCA" in capsys.readouterr().out


def test_tambah_lalu_laporan(tmp_path, monkeypatch, capsys):
    # Tes end-to-end sejati: dua invokasi main() terpisah, state (posisi.csv)
    # persisten di antaranya - membuktikan tambah_posisi menulis dan
    # cetak_laporan membaca lokasi file yang sama.
    monkeypatch.chdir(tmp_path)
    (tmp_path / "posisi.csv").write_text("ticker,lot,harga_beli\n")
    (tmp_path / "harga.csv").write_text(
        "ticker,tanggal,close\n"
        "BBCA,2025-01-01,9800\n"
        "BBCA,2025-01-02,9900\n"
    )

    main(["tambah", "BBCA", "10", "9500"])
    capsys.readouterr()  # buang output "berhasil ditambahkan"

    main(["laporan"])

    assert "BBCA" in capsys.readouterr().out


def test_hapus_ticker(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "posisi.csv").write_text("ticker,lot,harga_beli\nBBCA,10,9500\n")
    (tmp_path / "harga.csv").write_text(
        "ticker,tanggal,close\n"
        "BBCA,2025-01-01,9800\n"
        "BBCA,2025-01-02,9900\n"
    )

    main(["hapus", "BBCA"])
    capsys.readouterr()  # buang output "berhasil dihapus"

    main(["laporan"])

    assert "BBCA" not in capsys.readouterr().out


def test_tambah_tanpa_argumen_ditolak(capsys):
    with pytest.raises(SystemExit) as info:
        main(["tambah"])

    assert info.value.code == 2
    assert "usage" in capsys.readouterr().err.lower()


def test_subcommand_tidak_dikenal_ditolak(capsys):
    with pytest.raises(SystemExit) as info:
        main(["jual"])

    assert info.value.code == 2
    assert "usage" in capsys.readouterr().err.lower()


def test_smoke_interpreter_segar(tmp_path):
    # Satu-satunya tes yang benar-benar mengeksekusi baris
    # if __name__ == "__main__": dan membuktikan program bisa lahir, hidup,
    # dan mati dengan exit code 0 di interpreter segar - bukan dipanggil
    # langsung dalam proses pytest seperti tes lain di file ini.
    (tmp_path / "posisi.csv").write_text("ticker,lot,harga_beli\nBBCA,10,9500\n")
    (tmp_path / "harga.csv").write_text(
        "ticker,tanggal,close\n"
        "BBCA,2025-01-01,9800\n"
        "BBCA,2025-01-02,9900\n"
    )

    hasil = subprocess.run(
        [sys.executable, str(PATH_PORTOFOLIO_PY), "laporan"],
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )

    assert hasil.returncode == 0
