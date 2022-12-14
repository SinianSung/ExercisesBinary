from math import log2


class Bitpattern():
    bp = list()
    stellen = 8
    value = 0
    typ = ""

    def __init__(self, data, stellen=8):
        self.stellen = stellen
        self.value = data
        if isinstance(data, int):
            if data >= 0:
                self.bp = self.binaerdarstellung(data, self.stellen)
                self.typ = "unsigned"
            else:
                x = Bitpattern(-data, self.stellen)
                x.komplement()
                one = Bitpattern(1, self.stellen)
                self.bp = (x + one).bp
                self.typ = "signed"
        elif isinstance(data, str):

            self.bp = self.binaerdarstellung(ord(data), self.stellen)
            self.typ = "char"
        elif isinstance(data, float):
            exponent = int(log2(abs(data))) + 127
            bitpattern_exponent = self.binaerdarstellung(exponent, 8)
            if data > 0:
                signbit = [0]
            else:
                signbit = [1]
            data = abs(data)

            gebrochen = data / (2**(exponent-127))
            bitpattern_mantisse = self.__bitAlgFrac(gebrochen, 24)[1:]
            self.bp = [*signbit,*bitpattern_exponent,*bitpattern_mantisse]
            self.stellen = 32
            self.typ = "float"
        elif isinstance(data, bool):
            self.typ = "boolean"
            if data:
                self.bp = self.binaerdarstellung(1, self.stellen)
            else:
                self.bp = self.binaerdarstellung(0, self.stellen)

    def __str__(self):
        if self.bp == None:
            return
        out = ">"
        for bit in self.bp:
            out += str(bit)
        out += "<"
        return out

    def __repr__(self):
        return self.bp, self.stellen, self.value, self.typ

    def latex(self):
        if self.bp == None:
            return
        out = ""
        for bit in self.bp:
            out += str(bit)
        out += "_2"
        return out

    def komplement(self):
        kompl = []
        if self.bp == None:
            return
        for i in self.bp:
            if i == 0:
                kompl.append(1)
            else:
                kompl.append(0)
        self.bp = kompl

    def binaerdarstellung(self, zahl, stellen):
        """
        Algorithmus mit Hilfe der Zweierpotenzen
        zahlen:  ganzzahl die konvertiert werden soll
        stellen:    anzahl der stellen der bin??tzahl
        return liste mit den bits, 
        """
        if zahl >= 1 << (stellen+1):
            return
        zweierpotenzen = [2**x for x in range(stellen)[::-1]]
        bitpattern = []
        for p in zweierpotenzen:
            if zahl >= p:
                bitpattern.append(1)
                zahl = zahl - p
            else:
                bitpattern.append(0)
        return bitpattern

    def __bitAlgFrac(self, z: float, stellen: int):
        bitpat = []
        for i in range(stellen):
            if z<1:
                bitpat.append(0)
            else:
                bitpat.append(1)
                z=z-1
            z *= 2
        return bitpat

    def padding(self, stellen):
        pad = [0 for i in range(stellen)]
        if self.bp == None:
            return
        self.bp = pad + self.bp

    def __add__(self, other):
        m = max(self.stellen, other.stellen)
        if m > self.stellen:
            bp1 = self.padding(m-self.stellen)[::-1]
            bp2 = other.bp[::-1]
        elif m < other.stellen:
            bp1 = other.padding(m-other.stellen)[::-1]
            bp2 = self.bp[::-1]
        else:
            bp1 = self.bp[::-1]
            bp2 = other.bp[::-1]
        carry = 0
        sum = []
        for i in range(m):
            digit = carry + bp1[i] + bp2[i]
            if digit == 0 or digit == 1:
                sum.append(digit)
                carry = 0
            elif digit == 2:
                sum.append(0)
                carry = 1
            elif digit == 3:
                sum.append(1)
                carry = 1
        if carry == 1 and self.value*other.value > 0:
            print("Overflow")
        s = Bitpattern(0, m)
        s.value = self.value + other.value
        s.bp = sum[::-1]
        return s

    def __sub__(self, other):
        minuend = self
        subtrahend = Bitpattern(-other.value, other.stellen)
        erg = minuend + subtrahend
        erg.value = self.value - other.value
        return erg

    def decode(self, art="unsigned"):
        if art == "unsigned":
            pass
        elif art == "signed":
            pass
        elif art == "char":
            pass
        elif art == "float":
            pass
        else:
            pass


def main():

    x = Bitpattern(1.7, 32)
    print(x)


if __name__ == "__main__":
    main()
