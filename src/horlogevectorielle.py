#!/usr/bin/python3

class HorlogeVect():
    def __init__(self, size : int = None, index : int = None, _str : str = None):
        # L'horloge commence à zéro
        self.index = index
        if _str == None:
            self.hlg = [0] * size
            self.size = size
        else :
            self.hlg = list(map(int,_str.split(',')))
            self.size = len(self.hlg)

    
    # Màj de l'horloge, h <- max(h_rcv, h) + 1  
    # si h_rcv != None, incrémentation sinon
    def incr(self, h_rcv = None) -> None:
        if h_rcv != None:
            for i in range(self.size):
                self.hlg[i] = max(self.hlg[i], h_rcv.hlg[i])
        self.hlg[self.index] += 1
    
    def val(self):
        return self.hlg
    def __str__(self):
        return ','.join(map(str,self.hlg))
