from conversor2 import *

oks = noks = 0

for i, line in enumerate(open("test.numbers", "r")):
    
    numero, base = line.split()
    numero = numero.strip('0').lower()
    base = int(base)
    print(f"{i+1:3} - ({base}) {numero} --> ", end="")

    c = Conversor(numero, base)
    c3 = c.to_base(base)
    
    if numero != c3.numeroN:
        print(f"ERROR: {c3.numeroN}") 
        noks += 1
    else:
        print("OK!")
        oks += 1

    #if i == 100:
    #    break

print(f"Aciertos = {float(oks)*100/(oks+noks)}% ({oks=}, {noks=})")