import os
import json
from pathlib import Path

from dotenv import load_dotenv
from azure.eventhub import EventHubConsumerClient


load_dotenv()

CONNECTION_STRING = os.getenv(
    "AZURE_EVENT_HUB_CONNECTION_STRING"
)

EVENT_HUB_NAME = os.getenv(
    "AZURE_EVENT_HUB_NAME"
)

CONSUMER_GROUP = "$Default"


STREAM_PATH = Path(
    "data/bronze/streaming"
)

STREAM_PATH.mkdir(
    parents=True,
    exist_ok=True
)

ARQUIVO_SAIDA = (
    STREAM_PATH
    / "eventos_azure.jsonl"
)


def on_event(partition_context, event):

    evento = json.loads(
        event.body_as_str(
            encoding="UTF-8"
        )
    )

    with open(
        ARQUIVO_SAIDA,
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

    print(
        "[RECEBIDO AZURE]",
        evento
    )

    partition_context.update_checkpoint(
        event
    )


consumer = (
    EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENT_HUB_NAME
    )
)


print("\n====================================")
print("CONSUMER AZURE EVENT HUBS INICIADO")
print("====================================")
print("Aguardando eventos...")
print("Pressione CTRL+C para encerrar.\n")


try:

    with consumer:

        consumer.receive(
            on_event=on_event,
            starting_position="-1"
        )


except KeyboardInterrupt:

    print("\nConsumer Azure encerrado.")