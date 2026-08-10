# prosperidr

CLI sederhana untuk melacak portofolio saham IDX pribadi lewat command line: catat posisi (ticker, lot, harga beli), lalu lihat laporan untung/rugi berdasarkan harga historis (CSV lokal) atau harga real-time (yfinance).

## Untuk siapa

Investor ritel yang ingin melacak portofolio sendiri tanpa spreadsheet manual, dan siapa pun yang ingin melihat contoh proyek Python kecil dengan test suite (58 tes) yang menutupi jalur normal maupun jalur gagal.

## Instalasi

```
git clone https://github.com/jefridongkol09-spec/prosperidr.git
cd prosperidr
pip install -r requirements.txt
```

Dikembangkan dan diuji di Python 3.14. Koneksi internet hanya dibutuhkan untuk mode `--live` (lihat di bawah).

Di Windows, gunakan `py` alih-alih `python` kalau perintah `python` tidak dikenali (masalah stub Microsoft Store yang umum di instalasi Windows default) — semua contoh di README ini memakai `python`, ganti sendiri ke `py` kalau mengalami itu.

## Memulai

`posisi.csv` dan `harga.csv` adalah file kerja pribadi Anda — sengaja **tidak** ikut ter-commit (lihat `.gitignore`), supaya holdings sungguhan Anda tidak pernah tidak sengaja terpush ke repo publik. Repo ini hanya menyediakan contohnya:

```
copy contoh_posisi.csv posisi.csv
copy contoh_harga.csv harga.csv
```

(di Linux/macOS: `cp` alih-alih `copy`)

Tanpa langkah ini, `prosperidr laporan` akan keluar dengan pesan `PERINGATAN: file posisi.csv tidak ditemukan` ke stderr dan berhenti bersih (exit code 1) — bukan crash, tapi tetap tidak akan menampilkan apa pun sampai file kerja Anda ada.

## Pemakaian

Tiga subcommand: `laporan`, `tambah`, `hapus`.

### `laporan` — tampilkan portofolio

```
$ python portofolio.py laporan
TICKER       TANGGAL    HARGA    RET%         NILAI        MODAL          P/L    P/L%
-------------------------------------------------------------------------------------
BBRI      2025-01-04    4,600   +1.10    23,000,000   22,000,000   +1,000,000   +4.55
BBCA      2025-01-04    9,900   +2.06     9,900,000    9,500,000     +400,000   +4.21
BMRI      2025-01-04    6,200   +2.48    12,400,000   12,600,000     -200,000   -1.59
-------------------------------------------------------------------------------------
TOTAL                                    45,300,000   44,100,000   +1,200,000   +2.72
```

Tambahkan `--live` untuk mengambil harga real-time dari Yahoo Finance alih-alih `harga.csv`:

```
python portofolio.py laporan --live
```

Kalau live gagal untuk sebagian ticker (jaringan putus, ticker tidak dikenal), laporan tetap tampil dengan fallback ke `harga.csv` untuk ticker itu — ditandai `TOTAL*` beserta baris `PERINGATAN` yang menyebutkan tanggal mana saja yang bentrok, supaya angka campuran-vintage tidak pernah terlihat presisi padahal tidak.

Setiap kali `laporan` dijalankan (dengan atau tanpa `--live`), teks yang sama juga ditulis ke `laporan.txt` di direktori kerja saat ini, menimpa isi lama — bukan cuma tercetak ke layar.

### `tambah` — tambah atau perbesar posisi

```
$ python portofolio.py tambah TLKM 15 3700
Posisi TLKM berhasil ditambahkan
```

Kalau ticker sudah ada di posisi, `tambah` menggabungkannya: lot dijumlah, harga beli dirata-rata berbobot — bukan menambah baris duplikat.

### `hapus` — hapus posisi

```
$ python portofolio.py hapus TLKM
Posisi TLKM berhasil dihapus
```

## Menjalankan tes

```
pip install -r requirements.txt
pytest -v
```

```
58 passed in 3.45s
```

Test suite mencakup unit test murni (`test_algoritma.py`, `test_data.py`, `test_api_harga.py`, `test_portofolio.py`) dan tes CLI end-to-end (`test_cli.py`) yang memanggil `main()` langsung maupun lewat `subprocess` untuk membuktikan program bisa lahir dan mati bersih di interpreter segar.

## Keputusan desain

**Kenapa CSV, bukan database?** Skala datanya kecil (portofolio pribadi, puluhan baris) dan single-user — tidak ada kebutuhan concurrent access. CSV bisa dibuka dan diedit langsung di Excel atau teks editor tanpa tooling tambahan, yang penting untuk proyek yang harus tetap bisa diperiksa manual. Trade-off-nya nyata: `baca_posisi`/`baca_semua_harga` harus menjaga diri sendiri dari baris yang salah ketik atau kolom kurang (lihat cara keduanya melewati baris tak-valid dengan `PERINGATAN`, bukan crash), sesuatu yang gratis di database dengan skema.

**Kenapa fallback ke cache saat `--live` gagal, bukan gagal total?** Satu ticker yang gagal fetch (network error, delisting, rate limit) tidak seharusnya menggagalkan laporan untuk semua posisi lain. Tapi fallback diam-diam itu berbahaya kalau tidak ditandai — jadi setiap baris laporan punya kolom `TANGGAL` sendiri, dan `TOTAL` diberi label `TOTAL*` plus peringatan eksplisit begitu ada baris dengan tanggal yang tidak seragam. Prinsipnya: boleh pakai data lama, asal jujur bahwa itu data lama.

**Kebijakan harga tidak valid (nol atau NaN).** Harga saham yang sah di IDX tidak pernah bernilai nol — nol dan NaN sama-sama tanda data korup atau delisting, bukan pergerakan pasar, dan diperlakukan identik di kedua sumber data (CSV maupun API): dibuang kalau muncul di hari terbaru (belum settle), tapi menolak *seluruh* riwayat ticker itu kalau muncul di tengah deret. Alasannya bukan berlebihan — kalau satu hari bolong di tengah dibuang begitu saja, hari sebelum dan sesudahnya akan terlihat "berurutan" secara list padahal tidak, dan return harian akan terhitung lintas-gap seolah itu perubahan satu hari.

## Keterbatasan yang diketahui

`return_harian` mengasumsikan dua elemen terakhir dari daftar harga adalah dua hari berurutan. Ini benar selama kebijakan di atas berjalan (data tidak valid di tengah selalu ditolak penuh), tapi kalau titik data valid terakhir kebetulan jatuh tepat di ujung window karena alasan lain, label "return harian" bisa secara halus mewakili rentang yang lebih panjang dari satu hari. Perbaikan penuh butuh membawa tanggal berpasangan dengan harga di sepanjang pipa data, bukan tambalan — dicatat sebagai keputusan sadar untuk tidak dipaksakan masuk scope saat ini, bukan bug yang terlewat.
