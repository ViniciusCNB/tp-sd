import socket
import time
import ntplib
import threading
import os


class ServidorNTP:
    def __init__(self, host=os.getenv("HOST", "127.0.0.1"), porta=5000):
        self.host = host
        self.porta = porta
        self.tempo_atual = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.porta))
        self.socket.listen(5)

    def sincronizar_com_ntp(self):
        """Sincroniza o tempo do servidor com um servidor NTP real."""
        while True:
            try:
                cliente_ntp = ntplib.NTPClient()
                resposta = cliente_ntp.request("pool.ntp.org")
                self.tempo_atual = resposta.tx_time
                print(f"Servidor sincronizado com NTP: {time.ctime(self.tempo_atual)}")
            except Exception as e:
                print(f"Erro ao sincronizar com NTP: {e}")
            time.sleep(60)  # Sincroniza a cada minuto

    def atender_cliente(self, conexao, endereco):
        """Atende as solicitações de tempo dos clientes."""
        while True:
            try:
                # Recebe a solicitação do cliente
                dados = conexao.recv(1024)
                if not dados:
                    break

                # Envia o tempo atual
                tempo_envio = time.time()
                conexao.send(str(tempo_envio).encode())
                print(f"Tempo enviado para {endereco}: {time.ctime(tempo_envio)}")

            except Exception as e:
                print(f"Erro na comunicação com {endereco}: {e}")
                break

        conexao.close()

    def iniciar(self):
        """Inicia o servidor NTP."""
        # Inicia a thread de sincronização com NTP
        thread_sync = threading.Thread(target=self.sincronizar_com_ntp)
        thread_sync.daemon = True
        thread_sync.start()

        print(f"Servidor NTP iniciado em {self.host}:{self.porta}")

        # Loop principal para aceitar conexões
        while True:
            try:
                conexao, endereco = self.socket.accept()
                print(f"Nova conexão de {endereco}")

                # Cria uma nova thread para cada cliente
                thread_cliente = threading.Thread(
                    target=self.atender_cliente, args=(conexao, endereco)
                )
                thread_cliente.daemon = True
                thread_cliente.start()

            except Exception as e:
                print(f"Erro ao aceitar conexão: {e}")


if __name__ == "__main__":
    servidor = ServidorNTP()
    servidor.iniciar()
