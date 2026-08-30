import json
import time
from datetime import datetime
from pathlib import Path


# ==========================================
# CAMINHOS
# ==========================================

LOG_PATH = Path("logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)

ARQUIVO_LOG = LOG_PATH / "pipeline_monitoring.jsonl"

DATA_PATH = Path("data")


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def calcular_tamanho_pasta(pasta):
    """
    Calcula o tamanho total dos arquivos
    existentes dentro de uma pasta.
    """

    tamanho_total = 0
    quantidade_arquivos = 0

    if not pasta.exists():
        return 0, 0

    for arquivo in pasta.rglob("*"):

        if arquivo.is_file():
            tamanho_total += arquivo.stat().st_size
            quantidade_arquivos += 1

    return tamanho_total, quantidade_arquivos


def bytes_para_mb(valor):
    return round(valor / (1024 * 1024), 2)


def registrar_evento(evento):
    """
    Salva uma linha JSON no arquivo de log.
    """

    with open(
        ARQUIVO_LOG,
        "a",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            json.dumps(
                evento,
                ensure_ascii=False
            )
            + "\n"
        )


# ==========================================
# MONITORAMENTO
# ==========================================

def executar_monitoramento():

    inicio = time.time()

    timestamp_inicio = datetime.now()

    print("\n====================================")
    print("MONITORAMENTO DA PIPELINE")
    print("====================================")

    try:

        bronze = DATA_PATH / "bronze"
        silver = DATA_PATH / "silver"
        gold = DATA_PATH / "gold"

        # ----------------------------------
        # BRONZE
        # ----------------------------------

        tamanho_bronze, arquivos_bronze = (
            calcular_tamanho_pasta(bronze)
        )

        # ----------------------------------
        # SILVER
        # ----------------------------------

        tamanho_silver, arquivos_silver = (
            calcular_tamanho_pasta(silver)
        )

        # ----------------------------------
        # GOLD
        # ----------------------------------

        tamanho_gold, arquivos_gold = (
            calcular_tamanho_pasta(gold)
        )

        # ----------------------------------
        # VALIDAÇÕES BÁSICAS
        # ----------------------------------

        problemas = []

        if arquivos_bronze == 0:
            problemas.append(
                "Camada Bronze sem arquivos"
            )

        if arquivos_silver == 0:
            problemas.append(
                "Camada Silver sem arquivos"
            )

        if arquivos_gold == 0:
            problemas.append(
                "Camada Gold sem arquivos"
            )

        # ----------------------------------
        # STATUS
        # ----------------------------------

        if len(problemas) == 0:
            status = "SUCESSO"
        else:
            status = "ATENCAO"

        fim = time.time()

        duracao = round(
            fim - inicio,
            4
        )

        evento = {
            "timestamp": timestamp_inicio.isoformat(),
            "pipeline": "tech-challenge-fase-2",
            "status": status,
            "duracao_segundos": duracao,

            "bronze": {
                "quantidade_arquivos": arquivos_bronze,
                "tamanho_mb": bytes_para_mb(
                    tamanho_bronze
                )
            },

            "silver": {
                "quantidade_arquivos": arquivos_silver,
                "tamanho_mb": bytes_para_mb(
                    tamanho_silver
                )
            },

            "gold": {
                "quantidade_arquivos": arquivos_gold,
                "tamanho_mb": bytes_para_mb(
                    tamanho_gold
                )
            },

            "problemas": problemas
        }

        registrar_evento(evento)

        # ----------------------------------
        # SAÍDA NO TERMINAL
        # ----------------------------------

        print(
            f"Status: {status}"
        )

        print(
            f"Tempo de execução: "
            f"{duracao} segundos"
        )

        print("\n--- VOLUME PROCESSADO ---")

        print(
            f"Bronze: {arquivos_bronze} arquivos | "
            f"{bytes_para_mb(tamanho_bronze)} MB"
        )

        print(
            f"Silver: {arquivos_silver} arquivos | "
            f"{bytes_para_mb(tamanho_silver)} MB"
        )

        print(
            f"Gold: {arquivos_gold} arquivos | "
            f"{bytes_para_mb(tamanho_gold)} MB"
        )

        if problemas:

            print("\n--- ALERTAS ---")

            for problema in problemas:
                print(
                    f"[ATENÇÃO] {problema}"
                )

        else:

            print(
                "\n[OK] Pipeline sem problemas "
                "estruturais detectados."
            )

        print(
            f"\n[OK] Log salvo em: "
            f"{ARQUIVO_LOG}"
        )

        print("\n====================================")
        print("MONITORAMENTO CONCLUÍDO")
        print("====================================")

    except Exception as erro:

        fim = time.time()

        evento_erro = {
            "timestamp": timestamp_inicio.isoformat(),
            "pipeline": "tech-challenge-fase-2",
            "status": "ERRO",
            "duracao_segundos": round(
                fim - inicio,
                4
            ),
            "erro": str(erro)
        }

        registrar_evento(
            evento_erro
        )

        print(
            f"\n[ERRO] Falha no monitoramento:"
        )

        print(
            str(erro)
        )

        raise


# ==========================================
# EXECUÇÃO
# ==========================================

if __name__ == "__main__":
    executar_monitoramento()