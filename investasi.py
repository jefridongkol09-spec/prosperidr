harga_bitcoin = int(input("masukan harga bitcoin:")) 
jumlah_equity = int(input("masukan jumlah equity:")) 
modal = int(input("masukan modal:")) 
nilai_bitcoin = harga_bitcoin * jumlah_equity 
profit_loss = nilai_bitcoin - modal 
return_persen = profit_loss / modal * 100 
print(f"harga_bitcoin: Rp {harga_bitcoin:,}") 
print(f"jumlah_equity: {jumlah_equity}") 
print(f"modal        : Rp {modal:,}") 
print(f"nilai_bitcoin: Rp {nilai_bitcoin:,}") 
print(f"profit_loss  : Rp {profit_loss:,}") 
print(f"return       : {return_persen:.2f}%") 
if return_persen > 20:
    print("Status: PROFIT BESAR - pertimbangkan take profit sebagian")
elif return_persen > 0:
    print("Status: PROFIT KECIL - hold dan monitor")
elif return_persen == 0:
    print("Status: IMPAS")
elif return_persen >= -20:
    print("Status: RUGI KECIL - evaluasi posisi")
else:
    print("Status: RUGI BESAR - pertimbangkan cut loss") 