#!/usr/bin/python3

class Horloge():
    def __init__(self, val = 0):
        # L'horloge commence à zéro
        self.hlg = val
    
    # Màj de l'horloge, h <- max(h_rcv, h) + 1  
    # si h_rcv != None, incrémentation sinon
    def incr(self, h_rcv = None) -> None:
        if h_rcv != None:
            self.hlg = max(self.hlg, h_rcv.hlg) + 1
        else:
            self.hlg += 1
    
    def val(self):
        return self.hlg

    def __str__(self):
        return str(self.hlg)
