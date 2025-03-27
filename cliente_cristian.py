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
        self.tempo_local = time.time()
        self.ajuste = 0  # Diferença entre tempo local e servidor

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
            tempo_servidor = float(socket_cliente.recv(1024).decode())

            # Registra tempo de recebimento
            t1 = time.time()

            # Calcula RTT e offset
            rtt = t1 - t0
            delay = rtt / 2

            # Calcula o novo tempo ajustado
            tempo_ajustado = tempo_servidor + delay

            # Calcula o ajuste necessário
            self.ajuste = tempo_ajustado - time.time()

            print(f"Cliente {self.id_cliente}:")
            print(f"RTT: {rtt:.6f} segundos")
            print(f"Delay estimado: {delay:.6f} segundos")
            print(f"Ajuste necessário: {self.ajuste:.6f} segundos")

            socket_cliente.close()
            return True

        except Exception as e:
            print(f"Erro ao sincronizar com servidor: {e}")
            return False

    def ajustar_tempo_gradualmente(self):
        """Ajusta o tempo local gradualmente para evitar saltos bruscos."""
        if abs(self.ajuste) > 0:
            # Ajusta 10% da diferença a cada segundo
            ajuste_por_segundo = self.ajuste * 0.1
            self.tempo_local += ajuste_por_segundo
            self.ajuste -= ajuste_por_segundo

    def mostrar_tempo(self):
        """Mostra o tempo local atual."""
        while True:
            tempo_atual = time.time() + self.ajuste
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
            if self.obter_tempo_servidor():
                # Ajusta o tempo gradualmente por 10 segundos
                for _ in range(10):
                    self.ajustar_tempo_gradualmente()
                    time.sleep(1)
            time.sleep(60)  # Espera 60 segundos antes da próxima sincronização


if __name__ == "__main__":
    # O ID do cliente deve ser fornecido como argumento ao executar o script
    import sys

    id_cliente = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    cliente = ClienteCristian(id_cliente=id_cliente)
    cliente.iniciar()
