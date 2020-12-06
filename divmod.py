b11 = 11
n11 = 552310985215
n10 = 1561625508756

n11 = '552310985215'

print(f"{n11=}")
print(f"n10=" + f"{5*11**11+ 5*11**10+ 2*11**9+ 3*11**8+ 1*11**7+ 0*11**6+ 9*11**5+ 8*11**4+ 5*11**3+ 2*11**2+ 1*11+ 5}")



resto = 1     ## Cualquier cosa != 0
digitos = ''

while n10 > 0:
    s = f"divmod({n10=}, {b11=})"
    n10, resto = divmod(n10, b11)
    s = f"{n10=:.0f}, {resto=} = " + s
    print(s)
    digitos = str(resto) + ' ' + digitos

print(digitos)

resto = .235
exp = -1
bi11 = b11**exp
digitos2 = ''

while resto > 0.0000001:
    s = f"divmod({resto=:.20f}, {b11=:.2f}**{exp=:.2f}) ({b11**exp=:.2f})"
    n10d, resto = divmod(resto, bi11)
    s = f"{n10d=:.2f}, {resto=:.20f} = " + s
    print(s)
    exp -= 1
    bi11 = b11**exp
    digitos2 = digitos2 + ' ' + str(int(n10d))
    
print(digitos2)


## Los dígitos enteros están invertidos (y con un espacio al final
p_ent = digitos.split(' ')[:-1]

## Los dígitos p_ent están invertidos, el rango es el de las potencias de 0 a len(p_ent)-1
## lambda es la función que crea las potencias
suma_ent = sum(map(lambda x: int(x[0]) * b11 ** x[1], zip(p_ent[::-1], range(len(p_ent)))))

## Los decimales s
p_dec = digitos2.split(' ')[1:]

suma_dec = sum(map(lambda x: int(x[0]) * b11 ** -x[1], zip(p_dec, range(1, len(p_dec)))))

print(suma_ent + suma_dec)


