from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class PeriodoInventario:
    inicio: date
    fim: date

    def __post_init__(self):
        if self.inicio > self.fim:
            raise ValueError(
                "A data inicial não pode ser posterior à data final.")

    @property
    def inicio_formatado(self) -> str:
        return self.inicio.strftime("%d/%m/%Y")

    @property
    def fim_formatado(self) -> str:
        return self.fim.strftime("%d/%m/%Y")
