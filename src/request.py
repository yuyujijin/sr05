from enum import Enum

# Enum pour les états des sites


class NETStatus(Enum):
    REQUETE = "REQ"
    LIBERATION = "LIB"
    ACCUSE = "ACK"


class BASStatus(Enum):
    DEMANDESC = 0
    FINSC = 1
    DEBUTSC = 2
    UPDATE = 3


def BASStatusFromStr(s: str) -> BASStatus:
    for e, v in BASStatus.__members__.items():
        if f"BASStatus.{e}" == s:
            return v
    return None


def NETStatusFromStr(s: str) -> NETStatus:
    for e, v in NETStatus.__members__.items():
        if f"NETStatus.{e}" == s:
            return v
    return None
