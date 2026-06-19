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

        for _ in self.__tamanho:
            self.__pool.put(self.__conexao_banco())

        print(
            f"GerenciadorThreadBD inicializado com pool de conexões de tamanho: {self.__tamanho}"
            f"Número de núcleos da CPU: {os.cpu_count()}")

    def _calcular_tamanho(self, minimo, maximo):
        nucleos = os.cpu_count() or 1
        return min(max(nucleos * 2, minimo), maximo)

    def _pegar_conexao(self, timeout=5, tentativas=3):
        for tentativa_conexao in range(tentativas + 1):
            try:
                return self.__pool.get(timeout=timeout)
            except Empty:
                if tentativa_conexao == tentativas:
                    raise TimeoutError(
                        "Não foi possível obter uma conexão do pool após várias tentativas.")
                time.sleep(0.5)  # Espera um pouco antes de tentar novamente

    def _devolver_conexao(self, conexao):
        try:
            self.__pool.put(conexao)
        except Exception as e:
            # Tenta criar uma nova conexão se a devolução falhar
            self.__pool.put(self.__conexao_banco())

    def executar(self, funcao, *args, **kwargs):
        conexao = self._pegar_conexao()
        try:
            return funcao(conexao, *args, **kwargs)
        finally:
            self._devolver_conexao(conexao)

    def fechar(self):
        while not self.__pool.empty():
            try:
                self.__pool.get_nowait().close()
            except Exception as e:
                pass

    def trocar_bd(self, nova_conexao_banco):
        with self._lock:
            self.fechar()
            self.__conexao_banco = nova_conexao_banco
            for _ in range(self.__tamanho):
                self.__pool.put(self.__conexao_banco())
