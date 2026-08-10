import argparse
import sys

from data import (
    baca_semua_harga,
    baca_posisi,
    baca_tanggal_terakhir,
    tambah_posisi,
    hapus_posisi,
)
from api_harga import ambil_harga_online
from algoritma import (
    hitung_return_harian,
    cari_terbesar,
    cari_terkecil,
)


def analisis_saham(harga, lot, harga_beli):
    if not harga:
        return None

    harga_terakhir = harga[-1]

    semua_return_harian = hitung_return_harian(harga)

    # return harian = perubahan dua hari terakhir, berapa pun panjang window
    # harga yang masuk (4 hari dari harga.csv, 5 hari dari API, dst). Satu
    # titik data (atau semua transisi dilewati karena harga 0) berarti tidak
    # ada "kemarin" untuk dibandingkan - None ("tidak diketahui"), bukan 0.0
    # ("tidak bergerak") yang memfabrikasi kepastian yang tidak ada.
    return_harian = semua_return_harian[-1] if semua_return_harian else None

    harian_terbaik = cari_terbesar(semua_return_harian)
    harian_terburuk = cari_terkecil(semua_return_harian)

    nilai_pasar = harga_terakhir * lot * 100
    modal = harga_beli * lot * 100

    pl = nilai_pasar - modal
    pl_persen = (pl / modal) * 100

    return {
        "harga_terakhir": harga_terakhir,
        "return_harian": return_harian,
        "harian_terbaik": harian_terbaik,
        "harian_terburuk": harian_terburuk,
        "nilai_pasar": nilai_pasar,
        "modal": modal,
        "pl": pl,
        "pl_persen": pl_persen,
    }


def susun_laporan(laporan, total_nilai, total_modal):
    garis = "-" * 85
    baris = []

    baris.append(
        f"{'TICKER':<8}"
        f"{'TANGGAL':>12}"
        f"{'HARGA':>9}"
        f"{'RET%':>8}"
        f"{'NILAI':>14}"
        f"{'MODAL':>13}"
        f"{'P/L':>13}"
        f"{'P/L%':>8}"
    )
    baris.append(garis)

    if not laporan:
        baris.append("Tidak ada posisi dengan data harga untuk dilaporkan.")
        return "\n".join(baris)

    tanggal_unik = set()

    for ticker, hasil in laporan:
        tanggal_unik.add(hasil["tanggal_terakhir"])

        if hasil["return_harian"] is None:
            ret_str = f"{'n/a':>8}"
        else:
            ret_str = f"{hasil['return_harian']:>+8.2f}"

        baris.append(
            f"{ticker:<8}"
            f"{hasil['tanggal_terakhir']:>12}"
            f"{hasil['harga_terakhir']:>9,.0f}"
            f"{ret_str}"
            f"{hasil['nilai_pasar']:>14,.0f}"
            f"{hasil['modal']:>13,.0f}"
            f"{hasil['pl']:>+13,.0f}"
            f"{hasil['pl_persen']:>+8.2f}"
        )

    baris.append(garis)

    total_pl = total_nilai - total_modal
    total_pl_persen = (total_pl / total_modal) * 100

    campuran = len(tanggal_unik) > 1
    label_total = "TOTAL*" if campuran else "TOTAL"

    baris.append(
        f"{label_total:<8}"
        f"{'':>12}"
        f"{'':>9}"
        f"{'':>8}"
        f"{total_nilai:>14,.0f}"
        f"{total_modal:>13,.0f}"
        f"{total_pl:>+13,.0f}"
        f"{total_pl_persen:>+8.2f}"
    )

    if campuran:
        baris.append(
            "PERINGATAN: TOTAL* mencampur harga per tanggal berbeda"
            f" ({', '.join(sorted(tanggal_unik))}) - lihat kolom TANGGAL per baris"
        )

    return "\n".join(baris)


def ambil_data_harga(tickers, cache, cache_tanggal, live):
    hasil = {}

    for ticker in tickers:
        if live:
            data_live = ambil_harga_online(ticker)
            if data_live:
                hasil[ticker] = data_live
                continue
            print(
                f"PERINGATAN: gagal ambil harga live untuk {ticker}"
                f" - pakai data historis dari harga.csv",
                file=sys.stderr,
            )

        if ticker in cache:
            hasil[ticker] = {
                "harga": cache[ticker],
                "tanggal_terakhir": cache_tanggal.get(ticker),
            }

    return hasil


def cetak_laporan(live=False):
    portofolio = baca_semua_harga("harga.csv")
    if portofolio is None:
        raise SystemExit(1)

    tanggal_cache = baca_tanggal_terakhir("harga.csv")

    posisi = baca_posisi("posisi.csv")
    if posisi is None:
        raise SystemExit(1)

    data_harga = ambil_data_harga(posisi.keys(), portofolio, tanggal_cache, live)

    total_nilai = 0
    total_modal = 0
    laporan = []

    for ticker, info in posisi.items():
        lot = info["lot"]
        harga_beli = info["harga_beli"]

        entri = data_harga.get(ticker)
        if not entri or not entri.get("harga"):
            print(
                f"PERINGATAN: posisi {ticker} tidak punya data harga"
                f" - TOTAL TIDAK MENCAKUP POSISI INI",
                file=sys.stderr,
            )
            continue

        hasil = analisis_saham(
            entri["harga"],
            lot,
            harga_beli,
        )
        hasil["tanggal_terakhir"] = entri["tanggal_terakhir"]

        total_nilai += hasil["nilai_pasar"]
        total_modal += hasil["modal"]
        laporan.append((ticker, hasil))

    laporan.sort(key=lambda item: item[1]["pl"], reverse=True)

    teks = susun_laporan(laporan, total_nilai, total_modal)
    print(teks)
    with open("laporan.txt", "w", encoding="utf-8") as f:
        f.write(teks)


def main(argv=None):
    parser = argparse.ArgumentParser(description="prosperidr - portfolio tracker")
    subparsers = parser.add_subparsers(dest="command")

    parser_laporan = subparsers.add_parser("laporan")
    parser_laporan.add_argument(
        "--live",
        action="store_true",
        help="ambil harga real-time dari API, bukan harga.csv",
    )

    parser_tambah = subparsers.add_parser("tambah")
    parser_tambah.add_argument("ticker")
    parser_tambah.add_argument("lot", type=int)
    parser_tambah.add_argument("harga_beli", type=int)

    parser_hapus = subparsers.add_parser("hapus")
    parser_hapus.add_argument("ticker")

    args = parser.parse_args(argv)

    if args.command == "laporan":
        cetak_laporan(live=args.live)
    elif args.command == "tambah":
        berhasil = tambah_posisi("posisi.csv", args.ticker, args.lot, args.harga_beli)
        if berhasil:
            print(f"Posisi {args.ticker} berhasil ditambahkan")
        else:
            print(f"Gagal menambahkan posisi {args.ticker}")
    elif args.command == "hapus":
        berhasil = hapus_posisi("posisi.csv", args.ticker)
        if berhasil:
            print(f"Posisi {args.ticker} berhasil dihapus")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
