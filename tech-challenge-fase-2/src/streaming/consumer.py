import json
from pathlib import Path

from kafka import KafkaConsumer


# ==========================================
# CONFIGURAÇÃO
# ==========================================

KAFKA_SERVER = "localhost:9092"
TOPICO = "alfabetizacao-eventos"

BRONZE_STREAM_PATH = Path(
    "data/bronze/streaming"
)

BRONZE_STREAM_PATH.mkdir(
    parents=True,
    exist_ok=True
)

ARQUIVO_SAIDA = (
    BRONZE_STREAM_PATH
    / "eventos_alfabetizacao.jsonl"
)


# ==========================================
# CONSUMIDOR KAFKA
# ==========================================

consumer = KafkaConsumer(
    TOPICO,

    bootstrap_servers=KAFKA_SERVER,

    auto_offset_reset="earliest",

    enable_auto_commit=True,

    group_id="grupo-tech-challenge",

    value_deserializer=lambda valor: json.loads(
        valor.decode("utf-8")
    )
)


print("\n====================================")
print("CONSUMER KAFKA INICIADO")
print("====================================")
print(f"Tópico: {TOPICO}")
print(f"Destino Bronze: {ARQUIVO_SAIDA}")
print("Aguardando eventos...")
print("Pressione CTRL+C para encerrar.\n")


try:

    with open(
        ARQUIVO_SAIDA,
        "a",
        encoding="utf-8"
    ) as arquivo:

        for mensagem in consumer:

            evento = mensagem.value

            arquivo.write(
                json.dumps(
                    evento,
                    ensure_ascii=False
                )
                + "\n"
            )

            arquivo.flush()

            print(
                "[RECEBIDO]",
                evento
            )


except KeyboardInterrupt:

    print("\nConsumer encerrado.")

finally:

    consumer.close()