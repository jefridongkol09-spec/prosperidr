portofolio = {"BBCA": {"harga": 9200, "lembar": 100},
              "BBRI": {"harga": 4500, "lembar": 200},
              "BMRI": {"harga": 6700, "lembar": 150},
              "BRIS": {"harga": 3400, "lembar": 300},
              "BBNI": {"harga": 5600, "lembar": 250}}
total = 0
for kode, data in portofolio.items():
    modal = data["harga"] * data["lembar"]
    total += modal
    print(f"{kode} | Modal: Rp {modal:,}")

print(f"Total Modal: Rp {total:,}")