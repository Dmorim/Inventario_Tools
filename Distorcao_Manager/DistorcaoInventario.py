from dataclasses import dataclass


@dataclass(frozen=True)
class DistorcaoInventario:
    cdpro: list[str]
    nmpro: list[str]
    saldo_lan: list[float]
    saldo_pro: list[float]


@property
def campos_em_lista(self) -> list:
    return list(zip(
        self.cdpro,
        self.nmpro,
        self.saldo_lan,
        self.saldo_pro
    ))
