"""
Contiene las funciones de conversión de números en distintas bases
"""

DEBUG = False

def pprint(*arg, **kwarg):
    if DEBUG:
        print(*arg, **kwarg)

digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

## -------------------------------------------------------------------
def validar_base(base):
    """
    Se aceptan valores desde 2 a 36, y también las abreviaturas
    comunes para binario (bB), octal (oO), decimal (dD) y hexadecimal (hH)

    Devuelve -1 si la base no es válida
    """
    
    if base in 'bB': return 2
    if base in 'oO': return 8
    if base in 'dD': return 10
    if base in 'hH': return 16
    try:
        base = int(base)
    except:
        return -1
    if base >= 2 and base <= 36:
        return base
    return -1

## -------------------------------------------------------------------
def validar(num, base1, base2):
    """
    base1 y base2 deben ser distintas y valer entre 2 y 36
    El límite se debe a que no tengo más símbolos que estos:

        0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ

    Los dígitos en num deben ser los correspondientes
    al sistema de numeración. Ej.: base 2 -> [01]

    Se pueden incluir decimales (aunque ya veremos si
    somos capaces de implementar el algoritmo)
    """

    ## Función interior para abreviar la salida
    def out(status, num=None, base1=None, base2=None):
        return (status, num, base1, base2)
    

    ## Base no soportada o ambas iguales ----
    base1 = validar_base(base1)
    base2 = validar_base(base2)
    if base1 == -1:
        return out("Base1 (%s) incorrecta" % base1)
    if base2 == -1:
        return out("Base2 (%s) incorrecta" % base2)
    if base1 == base2:
        return out("Las dos bases son iguales")

    ## Validar que los dígitos de num son correctos para la base1 ----
    num = num.upper()                   ## Todo a mayúsculas para no enredar ----
    digitos_validos = digitos[:base1]
    for caracter in num:
        if not(caracter in digitos_validos or caracter == '.'):
            return out("El carácter %s no es válido "\
                        "en base %s" % (caracter, base1))

    ## Validar que haya como máximo un punto decimal ----
    len_num = len(num)
    len_num_no_punto = len(num.replace('.',''))
    if not(len_num == len_num_no_punto or len_num == len_num_no_punto + 1):
        return out("Hay más de un punto decimal en %s" % num)

    ## Parece que todo está bien ----
    return out("OK", num, base1, base2)

## -------------------------------------------------------------------
def convertir_a_base10(num, base_origen):
    """
    num es una cadena, base_origen es un número entre 2 y 36
    """
    base1 = int(base_origen)
    #pprint("Número: %s en base %s -> pasar a base %s" % (num, base1, base2))

    digitos_validos = digitos[:base1]
    pprint("Dígitos válidos:", digitos_validos)

    if '.' in num:
        parte_entera, parte_decimal = num.split(".")
    else:
        parte_entera, parte_decimal = num, ''
    pprint("La parte entera es %s, la decimal %s" % (parte_entera, parte_decimal))

    valor_total = 0
    for indice, digito in enumerate(parte_entera[::-1]):
        valor_digito = digitos_validos.index(digito)
        valor_decimal = valor_digito * base1**indice
        pprint(indice, digito, valor_decimal)
        valor_total += valor_decimal

    pprint()

    for indice, digito in enumerate(parte_decimal):
        valor_digito = digitos_validos.index(digito)
        valor_decimal = valor_digito * base1**(-indice-1)
        pprint(-indice-1, digito, valor_digito * base1**(-indice-1))
        valor_total += valor_decimal

    pprint("%s en base %s es %s en base %s" % (num, base1, valor_total, 10))
    return valor_total

## -------------------------------------------------------------------
def convertir_desde_base10(valor_total_b10, base_destino):
    base2 = int(base_destino)
    
    import math
    num2 = valor_total_b10
    exponentes = []
    set_exp_negativos = set()
    while True:
        log = math.log(num2, base2)
        exp = math.floor(log)
        pprint("El log en base %s de %s es %s" % (base2, num2, log))
        pprint("El floor de ese log es %s" % exp)
        resto = num2 - base2**exp
        exponentes.append(exp)
        if exp < 0:
            set_exp_negativos = set(x for x in exponentes if x < 0)
            pprint('set_exp_negativos', set_exp_negativos)
        num2 = resto

        pprint("El resto es %s" % resto)
        pprint("Los exponentes son %s" % exponentes)

        if resto <= 0 or len(set_exp_negativos) > 20:
            break

    import collections

    c = collections.Counter(exponentes)
    digitos_validos = digitos[:base2]

    exp = c.keys()
    min_key = min(exp)
    max_key = max(exp)

    salida = ""
    for k in range(min_key, max_key + 1):
        pprint(k, c.get(k, 0), digitos_validos[c.get(k, 0)])
        if k == 0 and salida != '':
            salida += '.'
        salida += digitos_validos[c.get(k, 0)]

    salida = salida[::-1] + ('...' if len(set_exp_negativos) > 20 else '')
    #pprint(salida, '(base %s)' % base2)

    return salida

## -------------------------------------------------------------------
## Hay que distinguir caso con decimal y sin decimal
def convertir(num, base1, base2):
    """
    num es una cadena (porque puede tener letras),
    las dos bases son números (NO ES CIERTO, pueden ser str (pero representando números))
    """
    return convertir_desde_base10(convertir_a_base10(num, base1), base2)


    ###digitos = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ###num = "38.5"
    ###base1 = 10
    ###base2 = 4
    base1 = int(base1)
    base2 = int(base2)

    pprint("Número: %s en base %s -> pasar a base %s" % (num, base1, base2))

    digitos_validos = digitos[:base1]
    pprint("Dígitos válidos:", digitos_validos)

    parte_entera, parte_decimal = num.split(".")
    pprint("La parte entera es %s, la decimal %s" % (parte_entera, parte_decimal))

    valor_total = 0
    for indice, digito in enumerate(parte_entera[::-1]):
        valor_digito = digitos_validos.index(digito)
        valor_decimal = valor_digito * base1**indice
        pprint(indice, digito, valor_decimal)
        valor_total += valor_decimal

    pprint()

    for indice, digito in enumerate(parte_decimal):
        valor_digito = digitos_validos.index(digito)
        valor_decimal = valor_digito * base1**(-indice-1)
        pprint(-indice-1, digito, valor_digito * base1**(-indice-1))
        valor_total += valor_decimal

    pprint("%s en base %s es %s en base %s" % (num, base1, valor_total, 10))


    import math
    num2 = valor_total
    exponentes = []
    set_exp_negativos = set()
    while True:
        log = math.log(num2, base2)
        exp = math.floor(log)
        pprint("El log en base %s de %s es %s" % (base2, num2, log))
        pprint("El floor de ese log es %s" % exp)
        resto = num2 - base2**exp
        exponentes.append(exp)
        if exp < 0:
            set_exp_negativos = set(x for x in exponentes if x < 0)
            pprint('set_exp_negativos', set_exp_negativos)
        num2 = resto

        pprint("El resto es %s" % resto)
        pprint("Los exponentes son %s" % exponentes)

        if resto <= 0 or len(set_exp_negativos) > 20:
            break

    import collections

    c = collections.Counter(exponentes)
    digitos_validos = digitos[:base2]

    exp = c.keys()
    min_key = min(exp)
    max_key = max(exp)

    salida = ""
    for k in range(min_key, max_key + 1):
        pprint(k, c.get(k, 0), digitos_validos[c.get(k, 0)])
        if k == 0:
            salida += '.'
        salida += digitos_validos[c.get(k, 0)]

    salida = salida[::-1] + ('...' if len(set_exp_negativos) > 20 else '')
    #pprint(salida, '(base %s)' % base2)

    return salida





















    
