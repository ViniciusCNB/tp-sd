import socket
import time
import threading


class ClienteCristian:
    def __init__(
        self,
        host_servidor="172.0.0.2",
        porta_servidor=5000,
        id_cliente=1
    ):
        self.host_servidor = host_servidor
        self.porta_servidor = porta_servidor
        self.id_cliente = id_cliente
        self.ajuste_total = 0  # Ajuste acumulado total
        self.ajuste_atual = 0  # Ajuste necessário na sincronização atual
        self.deriva_relogio = 0  # Taxa de deriva do relógio (segundos/minuto)
        self.ultima_sincronizacao = time.time()

    def obter_tempo_servidor(self):
        """Implementa o algoritmo de Cristian para sincronização."""
        try:
            # Cria conexão com o servidor
            socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_cliente.connect((self.host_servidor, self.porta_servidor))

            # Registra tempo de envio
            t0 = time.time()

            # Envia solicitação
            socket_cliente.send(b"GET_TIME")

            # Recebe resposta do servidor
            resposta = socket_cliente.recv(1024).decode()
            if not resposta:
                raise Exception("Resposta vazia do servidor")

            tempo_servidor = float(resposta)

            # Registra tempo de recebimento
            t1 = time.time()

            # Calcula RTT e offset
            rtt = t1 - t0
            delay = rtt / 2

            # Calcula o tempo do servidor ajustado pelo delay
            tempo_servidor_ajustado = tempo_servidor + delay

            # Calcula o tempo local sem ajustes
            tempo_local_bruto = time.time()

            # Calcula o novo ajuste necessário
            self.ajuste_atual = tempo_servidor_ajustado - tempo_local_bruto

            # Calcula a deriva do relógio se não for a primeira sincronização
            tempo_desde_ultima = tempo_local_bruto - self.ultima_sincronizacao
            if tempo_desde_ultima > 0:
                deriva_observada = (self.ajuste_atual - self.ajuste_total) / (
                    tempo_desde_ultima / 60
                )
                # Atualiza a deriva com um fator de suavização
                if self.deriva_relogio == 0:
                    self.deriva_relogio = deriva_observada
                else:
                    self.deriva_relogio = (
                        0.7 * self.deriva_relogio + 0.3 * deriva_observada
                    )

            # Aplica o ajuste imediatamente
            self.ajuste_total = self.ajuste_atual

            # Armazena o tempo desta sincronização
            self.ultima_sincronizacao = tempo_local_bruto

            print(f"Cliente {self.id_cliente}:")
            print(f"RTT: {rtt:.6f} segundos")
            print(f"Delay estimado: {delay:.6f} segundos")
            print(f"Ajuste necessário: {self.ajuste_atual:.6f} segundos")
            print(f"Deriva do relógio: {self.deriva_relogio:.6f} segundos/minuto")
            print(f"Tempo do servidor: {time.ctime(tempo_servidor)}")
            print(f"Tempo ajustado: {time.ctime(tempo_servidor_ajustado)}")

            socket_cliente.close()
            return True

        except Exception as e:
            print(f"Erro ao sincronizar com servidor: {e}")
            return False

    def obter_tempo_atual(self):
        """Retorna o tempo atual ajustado."""
        # Calcula o tempo desde a última sincronização
        tempo_desde_sincronizacao = time.time() - self.ultima_sincronizacao

        # Aplica o ajuste básico mais uma compensação pela deriva do relógio
        compensacao_deriva = (tempo_desde_sincronizacao / 60) * self.deriva_relogio
        tempo_ajustado = time.time() + self.ajuste_total - compensacao_deriva

        return tempo_ajustado

    def mostrar_tempo(self):
        """Mostra o tempo local atual."""
        while True:
            tempo_atual = self.obter_tempo_atual()
            print(
                f"Cliente {self.id_cliente} - "
                f"Tempo local: {time.ctime(tempo_atual)}"
            )
            time.sleep(60)  # Mostra o tempo a cada 60 segundos

    def iniciar(self):
        """Inicia o cliente."""
        # Thread para mostrar o tempo
        thread_mostrar = threading.Thread(target=self.mostrar_tempo)
        thread_mostrar.daemon = True
        thread_mostrar.start()

        # Loop principal de sincronização
        while True:
            self.obter_tempo_servidor()
            time.sleep(60)  # Espera 60 segundos antes da próxima sincronização


if __name__ == "__main__":
    # O ID do cliente deve ser fornecido como argumento ao executar o script
    import sys

    id_cliente = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cliente = ClienteCristian(id_cliente=id_cliente)
    cliente.iniciar()
