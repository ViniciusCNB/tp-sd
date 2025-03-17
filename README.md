# Sincronização de Relógios com Algoritmo de Cristian

Este projeto implementa o algoritmo de Cristian para sincronização de relógios físicos em uma rede distribuída.

## Requisitos

- Docker e Docker Compose
- Python 3.6 ou superior (para execução local)
- Biblioteca ntplib (para execução local)

## Execução com Docker (Recomendado)

1. Clone este repositório

2. Execute o sistema usando Docker Compose:
```bash
docker-compose up --build
```

Isso irá criar:
- 1 servidor NTP (IP: 172.20.0.2)
- 4 clientes com IPs distintos:
  - Cliente 1 (IP: 172.20.0.3)
  - Cliente 2 (IP: 172.20.0.4)
  - Cliente 3 (IP: 172.20.0.5)
  - Cliente 4 (IP: 172.20.0.6)

## Execução Local (Alternativa)

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Primeiro, inicie o servidor NTP:
```bash
python servidor_ntp.py
```

4. Em terminais diferentes, inicie vários clientes:
```bash
python cliente_cristian.py 1
python cliente_cristian.py 2
python cliente_cristian.py 3
python cliente_cristian.py 4
```

## Funcionamento

- O servidor mantém sincronização com um servidor NTP real (pool.ntp.org)
- Os clientes implementam o algoritmo de Cristian para sincronizar seus relógios
- A sincronização considera o atraso da rede (RTT/2)
- O ajuste do tempo é feito gradualmente para evitar saltos bruscos
- Os clientes mostram o tempo local atual e informações sobre a sincronização

## Detalhes da Implementação

- O servidor atualiza seu tempo a cada minuto via NTP
- Os clientes sincronizam a cada 5 segundos com o servidor
- O ajuste do tempo é feito gradualmente (10% da diferença por segundo)
- O RTT (Round Trip Time) é usado para calcular o delay da rede
- Cada cliente mostra seu tempo local atual e informações sobre o processo de sincronização
