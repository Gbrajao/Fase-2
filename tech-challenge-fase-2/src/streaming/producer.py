import json
import time
import random
from datetime import datetime

from kafka import KafkaProducer


# ==========================================
# CONFIGURAÇÃO DO KAFKA
# ==========================================

KAFKA_SERVER = "localhost:9092"
TOPICO = "alfabetizacao-eventos"


# ==========================================
# MUNICÍPIOS PARA GERAÇÃO DOS EVENTOS
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
# CONEXÃO COM O KAFKA
# ==========================================

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,

    value_serializer=lambda valor: json.dumps(
        valor,
        ensure_ascii=False
    ).encode("utf-8")
)


# ==========================================
# GERAÇÃO DO EVENTO
# ==========================================

def gerar_evento():

    local = random.choice(municipios)

    proficiencia = round(
        random.uniform(600, 900),
        2
    )

    evento = {
        "timestamp": datetime.now().isoformat(),
        "ano": 2024,
        "id_municipio": local["id_municipio"],
        "municipio": local["municipio"],
        "uf": local["uf"],
        "serie": 2,
        "proficiencia": proficiencia,
        "alfabetizado": proficiencia >= 743
    }

    return evento


# ==========================================
# ENVIO CONTÍNUO PARA O KAFKA
# ==========================================

print("\n====================================")
print("PRODUCER KAFKA INICIADO")
print("====================================")
print(f"Tópico: {TOPICO}")
print("Pressione CTRL+C para encerrar.\n")


try:

    while True:

        evento = gerar_evento()

        producer.send(
            TOPICO,
            value=evento
        )

        producer.flush()

        print(
            "[ENVIADO]",
            evento
        )

        time.sleep(2)


except KeyboardInterrupt:

    print("\nProducer encerrado.")

finally:

    producer.close()