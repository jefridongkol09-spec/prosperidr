import yfinance as yf


def ambil_harga_online(ticker, hari=5):
    try:
        saham = yf.Ticker(f"{ticker}.JK")
        riwayat = saham.history(period=f"{hari}d")
    except Exception:
        return None

    if riwayat.empty:
        return None

    return [round(float(harga), 2) for harga in riwayat["Close"]]
