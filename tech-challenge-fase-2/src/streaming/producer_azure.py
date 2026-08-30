import os
import json
import time
import random
from datetime import datetime

from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData


load_dotenv()

CONNECTION_STRING = os.getenv(
    "AZURE_EVENT_HUB_CONNECTION_STRING"
)

EVENT_HUB_NAME = os.getenv(
    "AZURE_EVENT_HUB_NAME"
)


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


def gerar_evento():

    local = random.choice(municipios)

    proficiencia = round(
        random.uniform(600, 900),
        2
    )

    return {
        "timestamp": datetime.now().isoformat(),
        "ano": 2024,
        "id_municipio": local["id_municipio"],
        "municipio": local["municipio"],
        "uf": local["uf"],
        "serie": 2,
        "proficiencia": proficiencia,
        "alfabetizado": proficiencia >= 743
    }


producer = EventHubProducerClient.from_connection_string(
    conn_str=CONNECTION_STRING,
    eventhub_name=EVENT_HUB_NAME
)


print("\n====================================")
print("PRODUCER AZURE EVENT HUBS INICIADO")
print("====================================")
print("Pressione CTRL+C para encerrar.\n")


try:

    while True:

        evento = gerar_evento()

        batch = producer.create_batch()

        batch.add(
            EventData(
                json.dumps(
                    evento,
                    ensure_ascii=False
                )
            )
        )

        producer.send_batch(batch)

        print(
            "[ENVIADO AZURE]",
            evento
        )

        time.sleep(2)


except KeyboardInterrupt:

    print("\nProducer Azure encerrado.")

finally:

    producer.close()