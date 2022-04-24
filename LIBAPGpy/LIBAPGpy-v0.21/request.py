from enum import Enum

# Enum pour les états des sites
class NETStatus(Enum):
    REQUETE = "REQ"
    LIBERATION = "LIB"
    ACCUSE = "ACK"

class BASStatus(Enum):
    DEMANDESC = 0
    FINSC = 1

def BASStatusFromStr(s : str) -> BASStatus:
    for e,v in BASStatus.__members__.items():
        if f"BASStatus.{e}" == s:
            return v
    return None