harga_saham = 2200
jumlah_lembar = 500
modal = 900000
nilai_saham = harga_saham * jumlah_lembar 
profit_loss = nilai_saham - modal 
return_persen = profit_loss / modal * 100 
print(f"Harga Saham   : Rp {harga_saham:,}")
print(f"Jumlah Lembar : {jumlah_lembar}")
print(f"Modal         : Rp {modal:,}")
print(f"Nilai Saham   : Rp {nilai_saham:,}")
print(f"Profit_Loss   : Rp {profit_loss:,}")
print(f"Return        : {return_persen:.2f}%") 