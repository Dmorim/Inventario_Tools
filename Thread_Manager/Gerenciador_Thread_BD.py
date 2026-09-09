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
        self._operacoes_condicao = threading.Condition(self._lock)
        self._operacoes_ativas = 0
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
        finally:
            try:
                conexao.rollback()
            except Exception:
                pass

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
        with self._operacoes_condicao:
            if self._fechando:
                raise RuntimeError(
                    'O gerenciador de conexões está sendo fechado.')
            self._operacoes_ativas += 1

        conexao = None
        try:
            conexao = self._pegar_conexao()
            return funcao(conexao, *args, **kwargs)
        finally:
            if conexao is not None:
                self._devolver_conexao(conexao)
            with self._operacoes_condicao:
                self._operacoes_ativas -= 1
                if self._operacoes_ativas == 0:
                    self._operacoes_condicao.notify_all()

    def aguardar_operacoes(self):
        """Aguarda as operações em andamento antes de uma manutenção."""
        with self._operacoes_condicao:
            while self._operacoes_ativas:
                self._operacoes_condicao.wait()

    def fechar(self):
        with self._lock:
            self._fechando = True
        self.aguardar_operacoes()
        with self._lock:
            while True:
                try:
                    conexao = self.__pool.get_nowait()
                except Empty:
                    break
                self._fechar_conexao(conexao)
