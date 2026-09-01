import os
import threading
import time
from queue import Queue, Empty


class GerenciadorThreadBD:
    def __init__(self, conexao_banco, minimo=2, maximo=50):
        self.__conexao_banco = conexao_banco
        self.__tamanho = self._calcular_tamanho(minimo, maximo)
        self.__pool = Queue()
        self._lock = threading.Lock()
        self._fechando = False

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
        except Exception:
            return False

        return True

    def _pegar_conexao(self, timeout=5, tentativas=3):
        for tentativa_conexao in range(tentativas + 1):
            try:
                conexao = self.__pool.get(timeout=timeout)
            except Empty:
                if tentativa_conexao == tentativas:
                    raise TimeoutError(
                        "Não foi possível obter uma conexão do pool após várias tentativas.")
                time.sleep(0.01)
                continue

            if not self._conexao_valida(conexao):
                try:
                    conexao.close()
                except Exception:
                    pass
                if tentativa_conexao == tentativas:
                    raise TimeoutError(
                        "Conexão inválida ou fechada foi descartada do pool.")
                continue

            return conexao

        raise TimeoutError(
            "Não foi possível obter uma conexão válida do pool.")

    def _devolver_conexao(self, conexao):
        if self._fechando:
            try:
                conexao.close()
            except Exception:
                pass
            return

        if not self._conexao_valida(conexao):
            try:
                conexao.close()
            except Exception:
                pass
            return

        try:
            self.__pool.put(conexao)
        except Exception:
            try:
                conexao.close()
            except Exception:
                pass

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
                try:
                    conexao.close()
                except Exception:
                    pass
