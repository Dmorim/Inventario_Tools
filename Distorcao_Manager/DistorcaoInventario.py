from dataclasses import dataclass


@dataclass(frozen=True)
class DistorcaoInventario:
    cdpro: tuple[str, ...]
    nmpro: tuple[str, ...]
    saldo_lan: tuple[float, ...]
    saldo_pro: tuple[float, ...]

    def __post_init__(self):
        if not (len(self.cdpro) == len(self.nmpro) == len(self.saldo_lan) == len(self.saldo_pro)):
            raise ValueError("Todos os campos devem ter o mesmo tamanho.")

        cdpro = tuple(self.cdpro)
        nmpro = tuple(self.nmpro)
        saldo_lan = tuple(self.saldo_lan)
        saldo_pro = tuple(self.saldo_pro)

        object.__setattr__(self, "cdpro", cdpro)
        object.__setattr__(self, "nmpro", nmpro)
        object.__setattr__(self, "saldo_lan", saldo_lan)
        object.__setattr__(self, "saldo_pro", saldo_pro)

    @property
    def campos_em_lista(self) -> list:
        return list(zip(
            self.cdpro,
            self.nmpro,
            self.saldo_lan,
            self.saldo_pro
        ))

    @property
    def tamanho(self) -> int:
        return len(self.cdpro)
