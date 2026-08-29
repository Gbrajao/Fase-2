import json
import time
import random
from datetime import datetime
from pathlib import Path


# ==========================================
# CONFIGURAÇÃO
# ==========================================

STREAM_PATH = Path("data/streaming")

STREAM_PATH.mkdir(
    parents=True,
    exist_ok=True
)

ARQUIVO_SAIDA = (
    STREAM_PATH
    / "eventos_alfabetizacao.jsonl"
)


# ==========================================
# DADOS PARA SIMULAÇÃO
# ==========================================

municipios = [
    {
        "id_municipio": "3550308",
        "municipio": "São Paulo",
        "uf": "SP"
    },
    {
        "id_municipio": "3304557",
        "municipio": "Rio de Janeiro",
        "uf": "RJ"
    },
    {
        "id_municipio": "1302603",
        "municipio": "Manaus",
        "uf": "AM"
    },
    {
        "id_municipio": "2927408",
        "municipio": "Salvador",
        "uf": "BA"
    },
    {
        "id_municipio": "2304400",
        "municipio": "Fortaleza",
        "uf": "CE"
    }
]


# ==========================================
# GERADOR DE EVENTO
# ==========================================

def gerar_evento():

    local = random.choice(
        municipios
    )

    proficiencia = round(
        random.uniform(600, 900),
        2
    )

    # O desafio informa 743 pontos como
    # ponto de corte de alfabetização.
    alfabetizado = (
        proficiencia >= 743
    )

    evento = {
        "timestamp": datetime.now().isoformat(),
        "id_municipio": local["id_municipio"],
        "municipio": local["municipio"],
        "uf": local["uf"],
        "serie": 2,
        "proficiencia": proficiencia,
        "alfabetizado": alfabetizado
    }

    return evento


# ==========================================
# SIMULAÇÃO DO STREAMING
# ==========================================

def executar_streaming(
    quantidade_eventos=10,
    intervalo_segundos=1
):

    print("\n==============================")
    print("INICIANDO STREAMING SIMULADO")
    print("==============================\n")

    with open(
        ARQUIVO_SAIDA,
        "a",
        encoding="utf-8"
    ) as arquivo:

        for numero in range(
            1,
            quantidade_eventos + 1
        ):

            evento = gerar_evento()

            arquivo.write(
                json.dumps(
                    evento,
                    ensure_ascii=False
                )
                + "\n"
            )

            arquivo.flush()

            print(
                f"Evento {numero}: "
                f"{evento}"
            )

            time.sleep(
                intervalo_segundos
            )

    print("\n==============================")
    print("STREAMING FINALIZADO")
    print("==============================")

    print(
        f"Eventos salvos em: "
        f"{ARQUIVO_SAIDA}"
    )


# ==========================================
# EXECUÇÃO
# ==========================================

if __name__ == "__main__":

    executar_streaming(
        quantidade_eventos=10,
        intervalo_segundos=1
    )