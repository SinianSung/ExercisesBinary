import random

from bitpattern import *
from maintenance import *

max = 250

aufgabenstellungen = ["Rechnen Sie die folgende Zahl ins Binärsystem um. ", \
    "Addieren Sie die folgenden Zahlen im Binärsystem.", \
    "Bestimmen Sie die Binärdarstellung der folgenden, negativen Zahl.", \
    "Bestimmen Sie die Binärdarstellung der folgenden Gleitkommazahl als 32Bit FloatingPoint."]

def umrechnung(signed = False):
    if signed:
        value = random.randint(-max, -4)
    else:
        value = random.randint(4,max)
    result = Bitpattern(value)
    return (aufgabenstellungen[0], value, result.latex())

def summen():
    value1 = Bitpattern(random.randint(4,max))
    value2 = Bitpattern(random.randint(4,max))
    erg = value1 + value2
    return (aufgabenstellungen[1], f"{value1.value} + {value2.value}", f"{value1.latex()} + {value2.latex()} = {erg.latex()}")

def negativ():
    wert = Bitpattern(random.randint(4, max))
    value_erg = Bitpattern(-wert.value)
    return (aufgabenstellungen[2], f"{wert.value}", f"{value_erg.value} \hat{{=}} {value_erg.latex()}")

def gleitkomma():
    wert = round(random.uniform(1.4, 20), random.randrange(1,4))
    value_erg = Bitpattern(wert)

    return (aufgabenstellungen[3], f"{wert}", f"{value_erg.latex()}")

def main(argv):
    arguments = getParameters(argv)
    exercises = []

    types ={'u': umrechnung, \
        's': summen, \
        'n': negativ, \
        'g': gleitkomma
        }

    list_of_types = check_types(types, arguments[1])

    for choice in list_of_types:
        for i in range(arguments[0]):
            exerc = types[choice]()
            exercises.append(exerc)
            exerc =""    

    createFile( exercises, arguments[2], 'Lösen Sie die Aufgaben') 

if __name__ == "__main__":
    main(sys.argv[1:])

# python .\aufgaben.py -n 20 -t u -T "Aufgaben Binärsystem"
