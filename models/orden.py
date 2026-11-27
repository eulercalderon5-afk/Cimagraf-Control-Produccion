"""Modelo de datos de una orden de producción."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Orden:
    codigo: str
    maquina: str
    procesadas: int
    merma: int
    inicio: datetime
    fin: datetime

    @property
    def buenas(self):
        return self.procesadas - self.merma

    @property
    def merma_pct(self):
        return round(self.merma * 100 / self.procesadas, 2)

    @property
    def minutos(self):
        return round((self.fin - self.inicio).total_seconds() / 60, 2)

    def como_dict(self):
        return {
            "codigo": self.codigo, "maquina": self.maquina,
            "procesadas": self.procesadas, "merma": self.merma,
            "buenas": self.buenas, "merma_pct": self.merma_pct,
            "inicio": self.inicio.strftime("%d-%m-%Y %H:%M"),
            "fin": self.fin.strftime("%d-%m-%Y %H:%M"),
            "minutos": self.minutos,
        }
