'''
Esto es una prueba mediante doctest
Se invoca desde el intérprete Python con

import doctest
doctest.testfile("conversor2.py")

o bien desde la línea de comandos como

python -m doctest -v conversor2.py

(esto último no funciona porque espera que esto sea un módulo python
y no reconoce las pruebas. Igual llevando este código al inicio...

'''
from decimal import Decimal, getcontext

class Conversor:
    '''
    >>> c = Conversor('10', 10)
    >>> c.to_base(16)
    Conversor('a', 16)

    >>> c = Conversor('.13f', 16)
    >>> c
    Conversor('.13f', 16)

    >>> c.exp10E, c.exp10D
    (0, -12)

    >>> c = Conversor('123F.4A2', 16)
    >>> c
    Conversor('123f.4a2', 16)

    >>> c.numeroN, c.baseN
    ('123f.4a2', 16)

    >>> c.pN_ent, c.pN_dec
    ('123f', '4a2')

    >>> c.listaNE, c.listaND
    ([Decimal('1'), Decimal('2'), Decimal('3'), Decimal('15')], [Decimal('4'), Decimal('10'), Decimal('2')])

    >>> c.num10E, c.num10D, c.num10
    (Decimal('4671'), Decimal('0.289550781250'), Decimal('4671.289550781250'))

    #>>> c.to_base(10)
    #Conversor('194', 10)

    >>> c = Conversor('ABC', 10)
    Traceback (most recent call last):
    AttributeError: Los dígitos de 'ABC' están fuera de rango para la base 10
    
    >>> c = Conversor('ABC', 100)
    Traceback (most recent call last):
    AttributeError: La base numérica es 100, y debería estar entre 2 y 36.
    
    
    
    '''

    ## Los dígitos para la conversión a su valor numérico (y viceversa) ----
    ## Uso el asterisco para desarrollar el iterador range() ----
    digitos = ''.join(chr(n)
                  for n in [*range(ord('0'), ord('9')+1)] +
                           [*range(ord('a'), ord('z')+1)]
                  )
    base_min = 2
    base_max = 36   ## TODO: eliminar este límite, que se debe solo a la imposibilidad de representar
                    ## dígitos mayores que 'z' usando solo números y letras. Si pones una presentación
                    ## estándar solo de ordinales para los casos superiores, no necesitas límite superior ----

    def __init__(self, numeroN: str, baseN: str):
        Conversor._validar_base(baseN)
        Conversor._validar_numero(numeroN, baseN)
        self.numeroN = numeroN.lower()  ## IMPORTANTE
        self.baseN = baseN

        getcontext().prec = 99 # len(self.numeroN)

        self.pN_ent, self.pN_dec = self._separar_decimales()
        self.listaNE = self._to_list(self.pN_ent)
        self.listaND = self._to_list(self.pN_dec)
        self.num10E = self._to_ent()
        self.num10D = self._to_dec()
        self.num10 = self.num10E + self.num10D
        self.exp10E = self._max_exp10()
        self.exp10D = self._min_exp10()

        precision = self.exp10E - self.exp10D
        getcontext().prec = precision if precision > 1 else 1

    def __repr__(self):
        return f"Conversor('{self.numeroN}', {self.baseN})"
    
    def _validar_base(baseN: int):
    ## Comprueba que la base está en sus límites
        '''
        Función de la clase, no de la instancia 

        ## Comprueba que la base está entre los límites permitidos ----
        >>> c = Conversor('123', 4)
        >>> Conversor._validar_base(2)
        >>> Conversor._validar_base(36)
        >>> Conversor._validar_base(15)

        ## Se espera un parámetro entero ----
        >>> Conversor._validar_base('A')
        Traceback (most recent call last):
        AttributeError: Se espera un parámetro entero

        >>> Conversor._validar_base(50)
        Traceback (most recent call last):
        AttributeError: La base numérica es 50, y debería estar entre 2 y 36.
        '''
        if isinstance(baseN, int):
            if Conversor.base_min <= baseN <= Conversor.base_max:
                pass
            else:
                raise AttributeError(f"La base numérica es {baseN}, y debería estar entre {Conversor.base_min} y {Conversor.base_max}.")
        else:
            raise AttributeError("Se espera un parámetro entero")

    def _validar_numero(numeroN: str, baseN: str):
    ## Comprueba un número en función de su base
        '''
        Función de clase

        >>> Conversor._validar_numero('ABC', 16)

        >>> Conversor._validar_numero('ABC', 10)
        Traceback (most recent call last):
        AttributeError: Los dígitos de 'ABC' están fuera de rango para la base 10

        >>> Conversor._validar_numero([], 16)
        Traceback (most recent call last):
        AttributeError: Se espera un numero (str) y una base de numeración (int)

        '''
        if isinstance(baseN, int) and isinstance(numeroN, str):
            if all(c in Conversor.digitos[:baseN] + '.' for c in numeroN.lower()):
                pass
            else:
                raise AttributeError(f"Los dígitos de '{numeroN}' están fuera de rango para la base {baseN}")
        else:
            raise AttributeError("Se espera un numero (str) y una base de numeración (int)")

    def _separar_decimales(self):
    ## Función interna para dividir la parte entera y la decimal
        '''
        Devuelve dos cadenas con la parte entera y decimal en cada una

        >>> c = Conversor('12345.6789', 10)
        >>> c._separar_decimales()
        ('12345', '6789')
        '''
        import re
        patron = re.compile(r'(\w+)?\.?(\w+)?')
        p_ent, p_dec = patron.match(self.numeroN).groups()
        if p_ent is None:
            p_ent = ''
        if p_dec is None:
            p_dec = ''
        return (p_ent, p_dec)

    def _to_list(self, numero: str) -> list:
    ## Traduce una cadena a la lista de sus valores numéricos.
        '''
        Función de clase
        No tiene en cuenta la base numérica
        Tampoco acepta puntos decimales
        En principio es una función interna que se usa para el resto de los cálculos
        independizando así el número de su representación como conjunto de dígitos

        >>> c = Conversor('aBcD1', 16)
        >>> c._to_list('aBcD1')
        [Decimal('10'), Decimal('11'), Decimal('12'), Decimal('13'), Decimal('1')]

        >>> c._to_list('.BcD1')
        Traceback (most recent call last):
        AttributeError: Dígito '.' no válido

        >>> c._to_list(['a', 'b', 'c'])
        Traceback (most recent call last):
        AttributeError: Se espera un numero (str)

        '''
        if isinstance(numero, str):
            numero = numero.lower()
            lista = list()
            for digito in numero:
                found = Conversor.digitos.find(digito)
                if found > -1:
                    lista.append(Decimal(found))
                else:
                    raise AttributeError(f"Dígito '{digito}' no válido")
            return lista
        else:
            raise AttributeError("Se espera un numero (str)")

    def _to_ent(self):
    ## Convierte una lista de números correspondientes a dígitos en base N a una cantidad decimal
        '''
        >>> c = Conversor('1234', 5)
        >>> c._to_ent()
        Decimal('194')
        '''
        le01 = self.listaNE[::-1]       ## digitos invertidos listaNE = '1234' -> le01 = '4321'
        le02 = len(le01)                ## 4
        if le02 == 0: 
            return Decimal('0')
        le03 = list(range(le02))        ## [0, 1, 2, 3]
        le04 = list(map(lambda x: (Decimal(self.baseN)**x), le03)) ## [N**0, ... N**3]
        le05 = list(zip(le01, le04))    ## combina ambas listas
        le06 = sum(x[0]*x[1] for x in le05) ## 4 * N**0 + 3 * N**1 + ...
        return le06

    def _to_dec(self):
    ## Interpreta '13F' como '.13F' y calcula su valor en base 10
        '''
        >>> c = Conversor('.13f', 16)
        >>> c._to_dec()
        Decimal('0.077880859375')
        '''
        ld01 = self.listaND             ## [1, 3, 15]
        ld02 = len(ld01)
        if ld02 == 0: 
            return Decimal('0')
        ld03 = list(range(-1, -ld02-1, -1))     ## [-1, -2, -3]
        ld04 = list(map(lambda x: (Decimal(self.baseN)**x), ld03)) ## [N**-1, ... N**-3]
        ld05 = list(zip(ld01, ld04))  ## combina ambas listas
        ld06 = sum(x[0]*x[1] for x in ld05) ## 4 * N**0 + 3 * N**1 + ...
        return ld06

    def _max_exp10(self):
    ## El exponente del dígito mayor
        import math
        if self.num10E > 0:
            return math.floor(math.log(self.num10E))
        else:
            return 0

    def _min_exp10(self):
    ## El exponente del dígito menor
        if self.num10D > 0:
            #if self.num10D < 1:
            digitos = len(str(self.num10D).split('.')[1])
            potencia = -digitos
            return potencia
        else:
            return 0

## INTERFAZ PUBLICO ================================================
    def validar_base(baseN: int):
        try:
            Conversor._validar_base(baseN)
            return True
        except:
            return False

    def validar_numero(numeroN: str, baseN: str) -> bool:
        try:
            Conversor._validar_numero(numeroN, baseN)
            return True
        except:
            return False

    def validar_digito(digito: str) -> bool:
    ## Comprueba que un dígito está en la lista de dígitos
        '''
        Un dígito tiene que ser str, tamaño 1 y estar en la lista de dígitos

        >>> Conversor.validar_digito('5')
        True
        >>> Conversor.validar_digito(5)
        False
        >>> Conversor.validar_digito(',')
        False
        >>> Conversor.validar_digito('Z')
        True
        >>> Conversor.validar_digito('a')
        True
        >>> Conversor.validar_digito('manolo')
        False
        >>> Conversor.validar_digito((2, 4))
        False
        >>> Conversor.validar_digito(None)
        False

        '''
        if isinstance(digito, str):
            if len(digito) == 1:
                if Conversor.digitos.find(digito.lower()) > 0:
                    return True
        return False

    def to_base(self, base_destino: int):
    ## De la representación interna en base 10 a una base N cualquiera
        '''
        >>> c = Conversor('1234', 5)
        >>> c.to_base(5)
        Conversor('1234', 5)

        >>> c.to_base(10)
        Conversor('194', 10)

        '''
        Conversor._validar_base(base_destino)
        if base_destino == self.baseN:
            return self
        if base_destino == 10:
            return Conversor(str(self.num10), 10)

        #self.num10 -> base N

        digitosE = []
        n10 = self.num10E

        ## Calcular la parte entera en la nueva base
        while n10 > 0:
            s = f"divmod({n10 = }, {base_destino = })"
            n10, resto = divmod(n10, base_destino)
            s = f"{n10 =:.0f}, {resto =} = " + s
            #print(s)
            digitosE.insert(0, int(resto))
   
        digitosD = []
        n10 = self.num10D
        error = 10**self.exp10D
        resto = n10
        exp = 1
        potenciaN = Decimal(base_destino) 

        ## Calcular la parte decimal en la nueva base
        while resto > error:
            s0 = f"potencia={potenciaN}\n"
            s2 = f"divmod({resto =:.20f}, {1/potenciaN =:.20f})"
            n10d, resto = divmod(resto, 1/potenciaN)
            s1 = f"{n10d =:.2f}, {resto =:.20f} = " 
            #print(s0 + s1 + s2)
            exp += 1
            potenciaN *= base_destino
            digitosD.append((int(n10d)))

        ## Conversión a cadena legible
        out = ''
        for chr in digitosE:
            out += Conversor.numero_a_digito(int(chr))
        
        if digitosD:
            out += '.'
            for chr in digitosD:
                out += Conversor.numero_a_digito(int(chr))

        return Conversor(out, base_destino)




        #return Conversor(self.numeroN, base_destino)









    def to_ent_dec(numero: str):
        '''
        De un número separa la parte entera de la decimal
        El número es str porque puede ser en base numérica > 10

        ## Doctests:
        >>> for x in ['TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMJ',
        ...           '.33333', '2.3333', '0.33232', '123456', '123456.']:
        ...    print(Conversor.to_ent_dec(x))
        ('TFQA73HYLOE6UGQQJ7NL', '.JQTXLK1UMJ')
        (None, '.33333')
        ('2', '.3333')
        ('0', '.33232')
        ('123456', '')
        ('123456', '')
        '''
        import re
        patron = re.compile(r'(\w+)?\.?(\w+)?')
        p_ent, p_dec = patron.match(numero).groups()
        if p_dec is None:
            p_dec = ''
        else:
            p_dec = '.' + p_dec
        return (p_ent, p_dec)

    def validar_digitos(numero, base):
        '''
        >>> Conversor.validar_digitos('TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMJ', 35)
        True
        >>> Conversor.validar_digitos('TFQA73HYLOE6UGQQJ7NL.JQTXLK1UMJ', 20)
        False
        '''
        return all(caracter.lower() in Conversor.digitos[:base] + '.' for caracter in numero)

    def digito_a_numero(c: str) -> int:
        '''
        >>> Conversor.digito_a_numero('z')
        35
        '''
        return Conversor.digitos.find(c.lower())

    def numero_a_digito(n:int) -> str:
        '''
        >>> Conversor.numero_a_digito(16)
        'g'
        '''
        return Conversor.digitos[n]


def test(n, b1, b2):
    c = Conversor(n, b1).to_base(b2)
    print(f"'{n}' en base {b1} es {c} en base {b2}")


if __name__ == "__main__":
    
    import doctest
    doctest.testmod(verbose=False)
    #doctest.run_docstring_examples(Conversor.__separar_decimales, globals(), verbose=True)
    print("====== FIN DOCTEST ======")

    test('10', 10, 16)


    '''
    c = Conversor('.13f', 16)
    print(c)
    print(c.numeroN)
    print(c.num10E)
    print(c.num10D)
    print(c.num10)

    c = Conversor('12345.678', 9)
    print(c.numeroN)
    print(c.num10E)
    print(c.num10D)
    print(c.num10)

    c = Conversor('1234e.678', 15)
    print(c.numeroN)
    print(c.num10E)
    print(c.num10D)
    print(c.num10)
'''