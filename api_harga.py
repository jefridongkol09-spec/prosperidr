import yfinance as yf


def ambil_harga_online(ticker, hari=5):
    try:
        saham = yf.Ticker(f"{ticker}.JK")
        riwayat = saham.history(period=f"{hari}d")
    except Exception:
        return None

    tutup = riwayat["Close"].dropna()

    if tutup.empty:
        return None

    return {
        "harga": [round(float(harga), 2) for harga in tutup],
        "tanggal_terakhir": tutup.index[-1].strftime("%Y-%m-%d"),
    }
