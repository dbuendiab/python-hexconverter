'''
Generar 100 números aleatorios en diferentes bases numéricas.
Con decimales
'''


import random
import decimal as dexx

digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def generate_base():
    return random.randint(2, 36)

def generate_digit(base: int):
    return random.choice(digitos[:base])

def cuantos_digitos_enteros(rango: int = 20):
    return random.randint(1, rango)

def cuantos_digitos_decimales(rango: int = 10):
    return random.randint(1, rango)

def con_decimales():
    return random.choice([False, True])

def generate_case(num_digitos_enteros: int=20, num_digitos_decimales: int=10):
    base = generate_base()
    num1 = cuantos_digitos_enteros(num_digitos_enteros)
    out = ''
    for _ in range(num1):
        out += generate_digit(base)
    if con_decimales():
        out += '.'
        num2 = cuantos_digitos_decimales(num_digitos_decimales)
        for _ in range(num2):
            out += generate_digit(base)
    return (out, base)

def valor_digito(c: str):
    return digitos.find(c.upper())

'''
def gen_primes():
    """Genera todos los números primos (con tiempo)"""
    primes = set()
    n = 2
    while True:
        if all(n % p > 0 for p in primes):
            primes.add(n)
            yield n
        n += 1

def factorizacion(N):
    gprimes = gen_primes()
    factors = []
    seguir = True
    for n in gprimes:
        while seguir:
            q, r = divmod(N, n)
            if r == 0:
                factors.append(n)
            else:
                break
            N = q
            if q == 1 and r == 0:
                seguir = False
                
        if not seguir:
            break
    return factors
'''

from division_exacta import *

with open("test.numbers", "w") as fp:

    for _ in range(1000):
        #try:
            numero, base = generate_case()
            fp.write(f"{numero} {base}\n")
            
            '''
            num10, preci = convertir_N_a_decimal(numero, base)
            print(f"Número origen: {numero} en base {base}")
            print(f"Se convierte en: {num10} en base 10")
            numN = convertir_decimal_a_N(str(num10), base)
            print(f"Número reconvertido: {numN}")
            if numero != numN:
                print("ERROR!!!")
            else:
                print("OK!")
            print()
            '''
        #except:
        #    pass



        
        
    
