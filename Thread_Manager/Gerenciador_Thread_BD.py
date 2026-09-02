import os
import threading
import time
from queue import Queue, Empty
from Outros.Logger.Get_Logger import get_logger


class GerenciadorThreadBD:
    def __init__(self, conexao_banco, minimo=2, maximo=50):
        self.__conexao_banco = conexao_banco
        self.__tamanho = self._calcular_tamanho(minimo, maximo)
        self.__pool = Queue()
        self._lock = threading.Lock()
        self._fechando = False
        self.logger = get_logger(__name__)

        self._preencher_pool()

    def _calcular_tamanho(self, minimo, maximo):
        nucleos = os.cpu_count() or 1
        return min(max(nucleos * 2, minimo), maximo)

    def _preencher_pool(self):
        for _ in range(self.__tamanho):
            self.__pool.put(self.__conexao_banco())

    def _conexao_valida(self, conexao):
        if conexao is None:
            return False

        try:
            if getattr(conexao, 'closed', False):
                return False
            cursor = conexao.cursor()
            try:
                cursor.execute('SELECT 1 FROM RDB$DATABASE')
            finally:
                cursor.close()
        except Exception:
            return False

        return True

    def _fechar_conexao(self, conexao):
        try:
            conexao.close()
        except Exception:
            pass

    def _criar_conexao_valida(self):
        conexao = self.__conexao_banco()
        if self._conexao_valida(conexao):
            return conexao
        self._fechar_conexao(conexao)
        raise ConnectionError('A nova conexão falhou no health-check.')

    def _pegar_conexao(self, timeout=5, tentativas=3):
        for tentativa_conexao in range(tentativas + 1):
            try:
                self.logger.debug(
                    f"Tentativa {tentativa_conexao + 1} de obter conexão do pool.")
                conexao = self.__pool.get(timeout=timeout)
            except Empty:
                if tentativa_conexao == tentativas:
                    raise TimeoutError(
                        "Não foi possível obter uma conexão do pool após várias tentativas.")
                time.sleep(0.01)
                continue

            if not self._conexao_valida(conexao):
                self._fechar_conexao(conexao)
                try:
                    return self._criar_conexao_valida()
                except Exception:
                    if tentativa_conexao == tentativas:
                        raise TimeoutError(
                            'Conexão inválida ou fechada foi descartada do pool.')
                    continue

            return conexao

        raise TimeoutError(
            "Não foi possível obter uma conexão válida do pool.")

    def _devolver_conexao(self, conexao):
        if self._fechando:
            self._fechar_conexao(conexao)
            return

        if not self._conexao_valida(conexao):
            self._fechar_conexao(conexao)
            try:
                self.__pool.put(self._criar_conexao_valida())
            except Exception:
                self.logger.exception(
                    'Não foi possível repor conexão inválida no pool.')
            return

        try:
            self.__pool.put(conexao)
        except Exception:
            self._fechar_conexao(conexao)

    def executar(self, funcao, *args, **kwargs):
        conexao = self._pegar_conexao()
        try:
            return funcao(conexao, *args, **kwargs)
        finally:
            self._devolver_conexao(conexao)

    def fechar(self):
        with self._lock:
            self._fechando = True
            while True:
                try:
                    conexao = self.__pool.get_nowait()
                except Empty:
                    break
                self._fechar_conexao(conexao)
