def analisa_investasi(harga, lembar, modal):
    nilai_saham = harga * lembar
    profit_loss = nilai_saham - modal
    return_persen = profit_loss / modal * 100
    if return_persen > 20:
        status = "PROFIT BESAR - pertimbangkan take profit sebagian"
    elif return_persen > 0:
        status = "PROFIT KECIL - hold dan monitor"
    elif return_persen == 0:
        status = "IMPAS"
    elif return_persen >= -20:
        status = "RUGI KECIL - evaluasi posisi"
    else:
        status = "RUGI BESAR - pertimbangkan cut loss"
    return f"Return:{return_persen:.2f}%, Status: {status}"
print(analisa_investasi(1500, 100, 200000))
print(analisa_investasi(2200, 500, 900000))   