import requests
import pandas as pd
from pathlib import Path


URL_IBGE = (
    "https://servicodados.ibge.gov.br/"
    "api/v1/localidades/municipios"
)

BRONZE_PATH = Path("data/bronze")
BRONZE_PATH.mkdir(
    parents=True,
    exist_ok=True
)

ARQUIVO_SAIDA = (
    BRONZE_PATH
    / "ibge_municipios.csv"
)


print("\n====================================")
print("INGESTÃO IBGE - MUNICÍPIOS")
print("====================================")


response = requests.get(
    URL_IBGE,
    timeout=60
)

response.raise_for_status()

dados = response.json()

print(
    f"Registros recebidos do IBGE: "
    f"{len(dados)}"
)


registros = []

for municipio in dados:

    microrregiao = (
        municipio.get("microrregiao")
        or {}
    )

    mesorregiao = (
        microrregiao.get("mesorregiao")
        or {}
    )

    uf = (
        mesorregiao.get("UF")
        or {}
    )

    regiao = (
        uf.get("regiao")
        or {}
    )

    registros.append(
        {
            "id_municipio": str(
                municipio["id"]
            ).zfill(7),

            "nome_municipio": municipio[
                "nome"
            ],

            "sigla_uf": uf.get(
                "sigla"
            ),

            "nome_uf": uf.get(
                "nome"
            ),

            "regiao": regiao.get(
                "nome"
            )
        }
    )


df = pd.DataFrame(registros)


print(
    f"Registros convertidos: {len(df)}"
)

print(
    "IDs duplicados:",
    df["id_municipio"]
    .duplicated()
    .sum()
)

print(
    "Valores nulos:",
    df.isnull()
    .sum()
    .sum()
)


df.to_csv(
    ARQUIVO_SAIDA,
    index=False,
    encoding="utf-8-sig"
)


print(
    f"[OK] Arquivo criado: "
    f"{ARQUIVO_SAIDA}"
)

print("\n====================================")
print("INGESTÃO IBGE CONCLUÍDA")
print("====================================")