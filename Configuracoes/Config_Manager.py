from configparser import ConfigParser
from pathlib import Path
from threading import RLock
import os
import tempfile


class AppConfig:
    def __init__(self, path: Path | None = None):
        self.path = path or Path(__file__).resolve().parents[1] / "config.ini"
        self._config = ConfigParser()
        self._lock = RLock()
        self._dirty = False

        if self.path.exists():
            self._config.read(self.path, encoding="utf-8")

    def get(self, section: str, key: str, fallback: str | None = None) -> str | None:
        with self._lock:
            return self._config.get(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str) -> None:
        with self._lock:
            if not self._config.has_section(section):
                self._config.add_section(section)

            value = str(value)
            if self._config.get(section, key, fallback=None) != value:
                self._config.set(section, key, value)
                self._dirty = True

    def save(self) -> None:
        with self._lock:
            if not self._dirty:
                return

            self.path.parent.mkdir(parents=True, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                delete=False,
                dir=self.path.parent,
            ) as temporary:
                self._config.write(temporary)
                temporary_path = Path(temporary.name)

            os.replace(temporary_path, self.path)
            self._dirty = False


_config = AppConfig()


def get_config() -> AppConfig:
    return _config


def salvar_diretorio(diretorio, name: str, last_dir):
    config = get_config()
    config.set(diretorio, name, last_dir)
    config.save()


def carregar_diretorio(diretorio, dir_busca):
    return get_config().get(diretorio, dir_busca, fallback=None)
