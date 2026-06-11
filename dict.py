portofolio = {"BBCA" : 9200, "BBRI" : 4500, "BMRI" : 6700, "BRIS" : 3400, "BBNI" : 5600}
print(portofolio["BBCA"])
print(len(portofolio)) # output: 5
for kode, harga in portofolio.items():
    print(f"{kode} : Rp {harga}")