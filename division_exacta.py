
'''
Esto es una prueba mediante doctest
Se invoca desde el intérprete Python con

import doctest
doctest.testfile("division_exacta.py")

o bien desde la línea de comandos como

python -m doctest -v division_exacta.py

(esto último no funciona porque espera que esto sea un módulo python
y no reconoce las pruebas. Igual llevando este código al inicio...

'''


digitos = ''.join(chr(n)
                  for n in [*range(ord('0'), ord('9')+1)] +
                           [*range(ord('A'), ord('Z')+1)]
                  )
## print(digitos)

def capturar_parte_entera_y_decimal(numero: str):
    '''
    De un número separa la parte entera de la decimal
    El número es str porque puede ser en base numérica > 10

    ## Doctests:
    >>> for x in ['TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMJ',
    ...           '.33333', '2.3333', '0.33232', '123456', '123456.']:
    ...    print(capturar_parte_entera_y_decimal(x))
    ('TFQA73HYLOE6UGQQJ7NL', 'JQTXLK1UMJ')
    (None, '33333')
    ('2', '3333')
    ('0', '33232')
    ('123456', '')
    ('123456', '')
    '''
    import re
    patron = re.compile(r'(\w+)?\.?(\w+)?')
    p_ent, p_dec = patron.match(numero).groups()
    if p_dec is None:
        p_dec = ''
    return (p_ent, p_dec)


def validar_digitos(numero, base):
    '''
    >>> validar_digitos('TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMJ', 35)
    True
    >>> validar_digitos('TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMJ', 20)
    False
    '''
    return all(caracter in digitos[:base] + '.'
               for caracter in numero
               )

def valor_digito(c: str) -> int:
    '''
    >>> valor_digito('Z')
    35
    '''
    return digitos.find(c)

def convertir_parte_entera(N_entera: str, base: int) -> int:
    import decimal as D
    exp = len(N_entera)-1
    out = D.Decimal('0')
    for c in N_entera:
        out += D.Decimal(valor_digito(c)) * D.Decimal(base) ** D.Decimal(exp)
        exp -= 1
    return out

def convertir_parte_decimal(N_decimal:str, base: int) -> float:
    import decimal as D 
    exp = -1
    #denominador = 10
    #numerador = 0
    out = D.Decimal('0')
    for c in N_decimal:
        out += D.Decimal(valor_digito(c)) * D.Decimal(base) ** D.Decimal(exp)
        exp -= 1 
    return out

def convertir_N_a_decimal(N: str, base: int) -> str:
    '''
    Conversión exacta: para la parte entera basta usar las potencias
    de la base, para la decimal hay que inventar algo
    '''
    import decimal as D
    import math

    base_origen = base
    #base_destino = 10

    if validar_digitos(N, base_origen) == False:
        return None

    p_ent, p_decimal = capturar_parte_entera_y_decimal(N)

    ## Los dígitos de la parte entera son potencias de la base,
    ## empezando por 0. Por tanto, la potencia mayor será
    max_exp = len(p_ent) - 1

    ## y la menor (siempre hablando de potencias de la base de N, no de 10)
    min_exp = len(p_decimal)

    ## Para la precisión, necesitamos tantos dígitos como resulten de
    ## sumar los dígitos de la parte entera del número convertido a decimal
    ## con los dígitos representativos de la parte decimal.

    ## Para lo primero, bastaría calcular el valor decimal
    ## del dígito de mayor orden y ver cuántos dígitos tiene:
    prec_p_ent = len(str(convertir_parte_entera(p_ent, base_origen)))
    #print(f"{prec_p_ent =}")

    ## Los dígitos de la parte decimal pueden ser infinitos, la
    ## forma de cortar es ver qué valor aporta la potencia menor
    ## y usar solo los dígitos necesarios para ese valor
    prec_p_decimal = -math.floor(math.log((base_origen ** (-min_exp)), 10))

    #print(f"{prec_p_decimal =}")
    #print(f"{math.floor(math.log(base ** (-min_exp), 10)) =}")

    ## Usaré números decimales de alta precisión
    ## Los dígitos que determina el error (prueba)
    D.getcontext().prec = prec_p_ent + prec_p_decimal
    #print(f"Precisión: {D.getcontext().prec}")

    ## Inicializo el resultado y el exponente que decrecerá según
    ## vayamos procesando los dígitos sucesivos
    numero10 = D.Decimal(0)
    exp = max_exp

    ## Bucle recorriendo los dígitos de la parte entera
    while p_ent:

        ## Cojo el primer carácter y guardo el resto
        c, p_ent = p_ent[0], p_ent[1:]

        ## Valor del dígito y cálculo de la conversión a decimal
        v = valor_digito(c)
        c_convertido = D.Decimal(v) * D.Decimal(base_origen) ** D.Decimal(exp)

        ## Añado al resultado
        numero10 += c_convertido

        ## Decremento el exponente
        exp -= 1

    ## Ahora el bucle recorriendo la parte decimal
    ## El exponente en este momento es -1
    while p_decimal:
        c, p_decimal = p_decimal[0], p_decimal[1:]
        v = valor_digito(c)
        c_convertido = D.Decimal(v) * D.Decimal(base_origen) ** D.Decimal(exp)
        numero10 += c_convertido
        exp -= 1

    ## Devuelvo el número y los decimales (para visualizar el valor correctamente)
    return numero10, prec_p_decimal

def convertir_decimal_a_N2(N: str, base: int) -> str:
    import decimal as D
    import math
    from collections import Counter

    base_origen = 10
    base_destino = base

    ## Los dígitos deben ser en base 10, aquí
    if validar_digitos(N, base_origen) == False:
        return None

    p_ent, p_decimal = capturar_parte_entera_y_decimal(N)
    #print(f"{p_ent =}, {p_decimal=}")

    ## Los dígitos de la parte entera son potencias de la base origen (10),
    ## empezando por 0. Por tanto, la potencia mayor será
    max_exp = len(p_ent) - 1

    ## y la menor (siempre hablando de potencias de la base de N, no de 10)
    min_exp = -len(p_decimal)
    #print(f"{max_exp =}, {min_exp=}")

    ## En el caso
    D.getcontext().prec = max_exp + 1 - min_exp
    #print(f"{D.getcontext().prec =}")

    ## Valor del último dígito decimal. Cuando el resto sea menor,
    ## ya no deberíamos seguir calculando.
    minimo_valor = '.' + '0' * (len(p_decimal)-1) + '1'
    min_val_f = float(minimo_valor)
    #print(f"{min_val_f=}, {minimo_valor=}")
    
    ## Método del logaritmo reiterativo

    #exponentes = []
    exponentes = Counter()

    num = D.Decimal(N)

    while True:
        log = math.log(num, base_destino)
        #print(f"{log=}")
        exp = math.floor(log)
        resto = num - D.Decimal(base_destino) ** exp
        #exponentes.append(exp)
        exponentes[exp] += 1
        #restos.append(resto)
        if resto < min_val_f:
            ## Redondeo: si resto > min_val_f / 2 -> añadir exp. anterior
            ## Contamos cuántos del último exponente hay:
            ## Si hay más de base_salida / 2:
            ## Eliminar todos esos últimos exponentes y añadir uno del anterior
            ## Si no los hay: eliminar sin hacer nada

            exp_actual = exp
            #exp_actual = exponentes[-1]
            exp_previo = exp_actual + 1
            num_exp_actual = exponentes[exp_actual]
            #num_exp_actual = sum(1 for x in exponentes if x == exp_actual)
            del exponentes[exp_actual]
            #exponentes = [x for x in exponentes if x != exp_actual]
            if num_exp_actual >= base_destino / 2:
                exponentes[exp_previo] += 1
                #exponentes.append(exp_previo)            
            break           ## Hace falta una condición de salida (error, etc.)
        num = resto
        #print(f"{num=}")

    #from collections import Counter
    #print(f"{exponentes=}")

    c = exponentes
    #c = Counter(exponentes)
    #print(f"{c=}")

    numeroN = ''
    minkey = min(c.keys())
    maxkey = max(c.keys())
    for digit in range(maxkey, minkey, -1):
	#print(digit, c[digit])
        repeticiones = c.get(digit, 0)
        numeroN += digitos[repeticiones]
        if digit == 0:
            numeroN += '.'

    return numeroN

def convertir_decimal_a_N(N: str, base: int) -> str:
    import decimal as D
    import math
    from collections import Counter

    base_origen = 10
    base_destino = base

    ## Los dígitos deben ser en base 10, aquí
    if validar_digitos(N, base_origen) == False:
        return None

    p_ent, p_decimal = capturar_parte_entera_y_decimal(N)

    ## Los dígitos de la parte entera son potencias de la base origen (10),
    ## empezando por 0. Por tanto, la potencia mayor será
    max_exp = len(p_ent) - 1

    ## y la menor (siempre hablando de potencias de la base de N, no de 10)
    min_exp = -len(p_decimal)

    D.getcontext().prec = len(N) # max_exp + 1 - min_exp


    ## Valor del último dígito decimal. Cuando el resto sea menor,
    ## ya no deberíamos seguir calculando.
    #minimo_valor = '.' + '0' * (len(p_decimal)-1) + '1'
    #min_val_f = float(minimo_valor)
    error_10 = base_origen ** min_exp
    #print(f"{min_val_f=}, {minimo_valor=}")
    
    ## Método del logaritmo reiterativo
    error_N = math.floor(math.log(error_10, base_destino))

    #exponentes = []
    exponentes = Counter()

    num = D.Decimal(N)

    while log > error_N:
        log = math.log(num, base_destino)
        #print(f"{log=}")
        exp = math.floor(log)
        resto = num - D.Decimal(base_destino) ** exp
        #exponentes.append(exp)
        exponentes[exp] += 1
        #restos.append(resto)
        if log < error_N:
            ## Redondeo: si resto > min_val_f / 2 -> añadir exp. anterior
            ## Contamos cuántos del último exponente hay:
            ## Si hay más de base_salida / 2:
            ## Eliminar todos esos últimos exponentes y añadir uno del anterior
            ## Si no los hay: eliminar sin hacer nada

            exp_actual = exp
            #exp_actual = exponentes[-1]
            exp_previo = exp_actual + 1
            num_exp_actual = exponentes[exp_actual]
            #num_exp_actual = sum(1 for x in exponentes if x == exp_actual)
            del exponentes[exp_actual]
            #exponentes = [x for x in exponentes if x != exp_actual]
            if num_exp_actual >= base_destino / 2:
                exponentes[exp_previo] += 1
                #exponentes.append(exp_previo)            
            break           ## Hace falta una condición de salida (error, etc.)
        num = resto
        #print(f"{num=}")

    #from collections import Counter
    #print(f"{exponentes=}")

    c = exponentes
    #c = Counter(exponentes)
    #print(f"{c=}")

    numeroN = ''
    minkey = min(c.keys())
    maxkey = max(c.keys())
    for digit in range(maxkey, minkey, -1):
	#print(digit, c[digit])
        repeticiones = c.get(digit, 0)
        numeroN += digitos[repeticiones]
        if digit == 0:
            numeroN += '.'

    return numeroN

if __name__ == "__main__":
    '''
    import doctest
    doctest.testmod(verbose=False)

    numero, base = 'TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMI', 35
    print(numero)
    num10, decimales = convertir_N_a_decimal(numero, base)
    formato = "{:." + str(decimales) + "f}"
    print(formato.format(num10))
    NumN = convertir_decimal_a_N(str(num10), base)
    print(NumN)
    print("-" * 80)
    
    numero, base = 'TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMJ', 35
    print(numero)
    num10, decimales = convertir_N_a_decimal(numero, base)
    formato = "{:." + str(decimales) + "f}"
    print(formato.format(num10))
    NumN = convertir_decimal_a_N(str(num10), base)
    print(NumN)
    print("-" * 80)

    numero, base = 'TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMK', 35
    print(numero)
    num10, decimales = convertir_N_a_decimal(numero, base)
    formato = "{:." + str(decimales) + "f}"
    print(formato.format(num10))
    NumN = convertir_decimal_a_N(str(num10), base)
    print(NumN)
    print("-" * 80)
    '''

    def test(numero: str, base: int):
        #numero, base = '120321101.130113011', 4
        print(numero)
        num10, decimales = convertir_N_a_decimal(numero, base)
        formato = "{:." + str(decimales) + "f}"
        print(formato.format(num10))
        NumN = convertir_decimal_a_N(str(num10), base)
        print(NumN)
        print("-" * 80)


    test('552310985215', 11)
        
    numero, base = '120321101.130113012', 4
    print(numero)
    num10, decimales = convertir_N_a_decimal(numero, base)
    formato = "{:." + str(decimales) + "f}"
    print(formato.format(num10))

    NumN = convertir_decimal_a_N(str(num10), base)
    print(NumN)
    print("-" * 80)

    numero, base = '120321101.130113013', 4
    print(numero)
    num10, decimales = convertir_N_a_decimal(numero, base)
    formato = "{:." + str(decimales) + "f}"
    print(formato.format(num10))
    NumN = convertir_decimal_a_N(str(num10), base)
    print(NumN)
    print("-" * 80)
