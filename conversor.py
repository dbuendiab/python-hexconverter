"""
Módulo para hacer conversiones entre sistemas de numeración

Permite convertir cantidades con decimales
Los sistemas de numeración admitidos van del 2 al 36

TODO

* Añadir tema precisión en los decimales de la conversión
* Añadir módulo de tests

HECHO

* Añadir repositorio github
* Añadir control de versiones git
* Añadir tratamiento estándar de parámetros: -h (ayuda), -v (verbose)


"""

import sys

import calculadora

## -------------------------------------------------------------------
MENSAJE_AYUDA = """
    CONVERSOR NUMÉRICO
    ------------------

    python conversor.py [-h] | <num> <base1> <base2> [-v]

    PARÁMETROS:

        num: La cadena de caracteres (representando un número) a convertir
        base1: Base numérica de num. Si no concuerda, da error
        base2: Base numérica a la que se quiere convertir num

        Sin parámetros, el programa se comporta en forma de bucle interactivo
        que terminará cuando el usuario introduzca (q)uit o (s)alir
    """

MENSAJE_INPUT = """
Introduce <número> <base1> <base2>
Para salir, pulsa [q]uit o [s]alir: 
"""

## -------------------------------------------------------------------
def ayuda():
    """
    Muestra el mensaje informativo de uso del programa
    """
    
    print(MENSAJE_AYUDA)
    
## -------------------------------------------------------------------
def main():
    """
    Función principal del programa
    """
    
    ## Ver si un parámetro es -v (y eliminarlo)
    if '-v' in sys.argv:
        calculadora.DEBUG = True
        del sys.argv[sys.argv.index('-v')]
    else:
        calculadora.DEBUG = False
        
    ## Los argumentos de la linea de comandos están en
    ## un objeto lista contenido en la variable sys.argv
    num_argumentos = len(sys.argv)

    ## El primer elemento es el nombre del programa, así que
    ## si la lista no tiene más que un elemento, es que no
    ## tiene parámetros en la línea de comandos -> modo interactivo
    if num_argumentos == 1:
        modo_interactivo()

    ## Si la lista tiene 4 elementos, los tres últimos son los parámetros
    ## Los pasamos al modo comando, para que haga los cálculos y salga
    elif num_argumentos == 4:
        numero = sys.argv[1]
        base1  = sys.argv[2]
        base2  = sys.argv[3]
        modo_comando(numero, base1, base2)
        
    ## Cualquier otra combinación de argumentos: mal -> info y salir
    else:
        ayuda()
    

## -------------------------------------------------------------------
def modo_interactivo():
    """
    Entra en un bucle donde pregunta al usuario los parámetros
    y calcula conversiones hasta que este decide salir.
    """
    
    while True:
        param = input(MENSAJE_INPUT)

        ## Para salir damos facilidades: vale SALIR o QUIT (en mayúsculas
        ## o minúsculas, una letra o varias.
        if param[0].upper() in 'SQ':
            break

        try:
            numero, base1, base2 = param.split()
        except:
            print("Número de parámetros incorrecto")
            
        modo_comando(numero, base1, base2)
  
## -------------------------------------------------------------------
def modo_comando(num, base1, base2):
    """
    Traslada los parámetros al módulo que hace los cálculos
    Se deja aquí porque esté en el mismo módulo que el
    modo interactivo
    """
    ok, num, base1, base2 = calculadora.validar(num, base1, base2)
    if  ok != 'OK':
        print("Error validación:", ok)
    else:
        resultado = calculadora.convertir(num, base1, base2)
        print("%s (base %s) = %s (base %s)" % (num, base1, resultado, base2))
        
        
## -------------------------------------------------------------------
if __name__ == '__main__':
    main()
