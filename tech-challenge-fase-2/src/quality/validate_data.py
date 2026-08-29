import pandas as pd
from pathlib import Path


SILVER_PATH = Path("data/silver")


def validar_duplicados(df, nome):
    duplicados = df.duplicated().sum()

    if duplicados == 0:
        print(f"[OK] {nome}: sem duplicados")
    else:
        print(
            f"[ATENÇÃO] {nome}: "
            f"{duplicados} duplicados"
        )


def validar_nulos_chave(df, coluna, nome):
    nulos = df[coluna].isnull().sum()

    if nulos == 0:
        print(
            f"[OK] {nome}: "
            f"chave {coluna} sem nulos"
        )
    else:
        print(
            f"[ERRO] {nome}: "
            f"{nulos} nulos em {coluna}"
        )


def validar_percentual(df, coluna, nome):
    valores = df[coluna].dropna()

    invalidos = valores[
        ~valores.between(0, 100)
    ]

    if len(invalidos) == 0:
        print(
            f"[OK] {nome}: "
            f"{coluna} entre 0 e 100"
        )
    else:
        print(
            f"[ERRO] {nome}: "
            f"{len(invalidos)} valores inválidos"
        )


def validar_relacionamento(
    df_origem,
    df_destino,
    chave,
    nome
):
    origem = set(
        df_origem[chave]
        .dropna()
        .astype(str)
    )

    destino = set(
        df_destino[chave]
        .dropna()
        .astype(str)
    )

    sem_correspondencia = origem - destino

    if len(sem_correspondencia) == 0:
        print(
            f"[OK] {nome}: "
            "todas as chaves possuem correspondência"
        )
    else:
        print(
            f"[ATENÇÃO] {nome}: "
            f"{len(sem_correspondencia)} "
            "chaves sem correspondência"
        )


print("\n====================================")
print("INICIANDO VALIDAÇÃO DE QUALIDADE")
print("====================================")


uf = pd.read_parquet(
    SILVER_PATH / "uf.parquet"
)

meta_brasil = pd.read_parquet(
    SILVER_PATH / "meta_brasil.parquet"
)

meta_uf = pd.read_parquet(
    SILVER_PATH / "meta_uf.parquet"
)

meta_municipio = pd.read_parquet(
    SILVER_PATH / "meta_municipio.parquet"
)

municipio = pd.read_parquet(
    SILVER_PATH / "municipio.parquet"
)

alunos = pd.read_parquet(
    SILVER_PATH / "alunos.parquet"
)


print("\n--- DUPLICADOS ---")

validar_duplicados(
    uf,
    "UF"
)

validar_duplicados(
    meta_brasil,
    "Meta Brasil"
)

validar_duplicados(
    meta_uf,
    "Meta UF"
)

validar_duplicados(
    meta_municipio,
    "Meta Município"
)

validar_duplicados(
    municipio,
    "Município"
)

validar_duplicados(
    alunos,
    "Alunos"
)


print("\n--- CHAVES ---")

validar_nulos_chave(
    uf,
    "sigla_uf",
    "UF"
)

validar_nulos_chave(
    meta_uf,
    "sigla_uf",
    "Meta UF"
)

validar_nulos_chave(
    meta_municipio,
    "id_municipio",
    "Meta Município"
)

validar_nulos_chave(
    municipio,
    "id_municipio",
    "Município"
)

validar_nulos_chave(
    alunos,
    "id_municipio",
    "Alunos"
)


print("\n--- PERCENTUAIS ---")

validar_percentual(
    uf,
    "taxa_alfabetizacao",
    "UF"
)

validar_percentual(
    meta_brasil,
    "taxa_alfabetizacao",
    "Meta Brasil"
)

validar_percentual(
    meta_uf,
    "taxa_alfabetizacao",
    "Meta UF"
)

validar_percentual(
    meta_municipio,
    "taxa_alfabetizacao",
    "Meta Município"
)

validar_percentual(
    municipio,
    "taxa_alfabetizacao",
    "Município"
)


print("\n--- RELACIONAMENTOS ---")

validar_relacionamento(
    meta_uf,
    uf,
    "sigla_uf",
    "Meta UF -> UF"
)

validar_relacionamento(
    meta_municipio,
    municipio,
    "id_municipio",
    "Meta Município -> Município"
)

validar_relacionamento(
    alunos,
    municipio,
    "id_municipio",
    "Alunos -> Município"
)


print("\n--- PROFICIÊNCIA ---")

ausentes = alunos[
    alunos["presenca"] == "Ausente"
]

presentes = alunos[
    alunos["presenca"] == "Presente"
]

print(
    "Proficiência nula entre ausentes:",
    ausentes["proficiencia"]
    .isnull()
    .sum()
)

print(
    "Proficiência nula entre presentes:",
    presentes["proficiencia"]
    .isnull()
    .sum()
)


print("\n====================================")
print("VALIDAÇÃO DE QUALIDADE CONCLUÍDA")
print("====================================")
uf_meta = set(
    meta_uf["sigla_uf"]
    .dropna()
    .astype(str)
)

uf_base = set(
    uf["sigla_uf"]
    .dropna()
    .astype(str)
)

faltantes_uf = sorted(
    uf_meta - uf_base
)

print(
    "\nSiglas da Meta UF sem correspondência em UF:",
    faltantes_uf
)