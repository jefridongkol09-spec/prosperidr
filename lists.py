portofolio = ['BBCA', 'BBRI', 'BMRI', 'BRIS', 'BBNI']
#              [0]     [1]      [2]     [3]    [4]
print(portofolio[0])  # Output: BBCA
print(portofolio[-1]) # output: BBNI
portofolio.append("BRIS")
print(len(portofolio)) # output: 5
for Saham in portofolio:
    print(f"Saham: {Saham}")