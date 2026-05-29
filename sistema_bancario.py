import threading
import time
import random


#  MEMÓRIA COMPARTILHADA

saldo = 1000.0  # variável compartilhada entre threads
lock = threading.Lock()  # mecanismo de sincronização
historico = []  # log compartilhado de transações

#  FUNÇÕES DAS THREADS

def depositar(nome, valor, repeticoes):
    """Thread de depósito — acessa e modifica saldo compartilhado."""
    global saldo
    for i in range(repeticoes):
        time.sleep(random.uniform(0.1, 0.4))  # simula tempo de processamento

        with lock:  # ← LOCK: região crítica
            saldo_anterior = saldo
            saldo += valor
            msg = (
                f"[{nome}] Depósito #{i+1}: +R${valor:.2f} | "
                f"Saldo: R${saldo_anterior:.2f} → R${saldo:.2f}"
            )
            historico.append(msg)
            print(msg)


def sacar(nome, valor, repeticoes):
    """Thread de saque — acessa e modifica saldo compartilhado."""
    global saldo
    for i in range(repeticoes):
        time.sleep(random.uniform(0.1, 0.4))  # simula tempo de processamento

        with lock:  # ← LOCK: região crítica
            if saldo >= valor:
                saldo_anterior = saldo
                saldo -= valor
                msg = (
                    f"[{nome}] Saque   #{i+1}: -R${valor:.2f} | "
                    f"Saldo: R${saldo_anterior:.2f} → R${saldo:.2f}"
                )
            else:
                msg = (
                    f"[{nome}] Saque   #{i+1}: ❌ Saldo insuficiente! "
                    f"(Saldo atual: R${saldo:.2f})"
                )
            historico.append(msg)
            print(msg)


def monitorar(intervalo, duracao):
    """Thread de monitoramento — lê saldo periodicamente (somente leitura)."""
    global saldo
    inicio = time.time()
    while time.time() - inicio < duracao:
        time.sleep(intervalo)
        with lock:
            print(
                f"\n  📊 [MONITOR] Saldo atual: R${saldo:.2f} | "
                f"Transações: {len(historico)}\n"
            )

#  PROGRAMA PRINCIPAL

if __name__ == "__main__":
    print("=" * 60)
    print("       🏦 SISTEMA BANCÁRIO CONCORRENTE")
    print("=" * 60)
    print(f"  Saldo inicial: R${saldo:.2f}")
    print(f"  Threads: Depósito | Saque | Monitor")
    print("=" * 60 + "\n")

    # Criação das threads
    t1 = threading.Thread(
        target=depositar, args=("Caixa-01", 200.0, 5), name="Deposito"
    )
    t2 = threading.Thread(target=sacar, args=("Caixa-02", 150.0, 5), name="Saque")
    t3 = threading.Thread(target=monitorar, args=(1.0, 5), name="Monitor")

    # Inicialização das threads
    t1.start()
    t2.start()
    t3.start()

    # Aguarda todas finalizarem
    t1.join()
    t2.join()
    t3.join()

    # Relatório final
    print("\n" + "=" * 60)
    print("              📋 RELATÓRIO FINAL")
    print("=" * 60)
    print(f"  Saldo inicial:  R$1000.00")
    print(f"  Saldo final:    R${saldo:.2f}")
    print(f"  Total de transações: {len(historico)}")
    print("=" * 60)