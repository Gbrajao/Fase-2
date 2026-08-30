import pandas as pd
from pathlib import Path


# ==========================================
# CAMINHOS
# ==========================================

SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")


print("\n====================================")
print("INICIANDO VALIDAÇÃO DE QUALIDADE")
print("====================================")


# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================

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

ibge = pd.read_parquet(
    SILVER_PATH / "ibge_municipios.parquet"
)

gold_ibge = pd.read_parquet(
    GOLD_PATH / "municipio_enriquecido_ibge.parquet"
)


# ==========================================
# DUPLICADOS
# ==========================================

print("\n--- DUPLICADOS ---")


bases = {
    "UF": uf,
    "Meta Brasil": meta_brasil,
    "Meta UF": meta_uf,
    "Meta Município": meta_municipio,
    "Município": municipio,
    "Alunos": alunos,
    "IBGE Municípios": ibge
}


for nome, df in bases.items():

    duplicados = df.duplicated().sum()

    if duplicados == 0:
        print(
            f"[OK] {nome}: sem duplicados"
        )
    else:
        print(
            f"[ATENÇÃO] {nome}: "
            f"{duplicados} duplicados"
        )


# ==========================================
# CHAVES
# ==========================================

print("\n--- CHAVES ---")


chaves = [
    ("UF", uf, "sigla_uf"),
    ("Meta UF", meta_uf, "sigla_uf"),
    (
        "Meta Município",
        meta_municipio,
        "id_municipio"
    ),
    (
        "Município",
        municipio,
        "id_municipio"
    ),
    (
        "Alunos",
        alunos,
        "id_municipio"
    ),
    (
        "IBGE Municípios",
        ibge,
        "id_municipio"
    )
]


for nome, df, coluna in chaves:

    nulos = df[coluna].isnull().sum()

    if nulos == 0:
        print(
            f"[OK] {nome}: chave "
            f"{coluna} sem nulos"
        )
    else:
        print(
            f"[ATENÇÃO] {nome}: "
            f"{nulos} valores nulos "
            f"na chave {coluna}"
        )


# ==========================================
# PERCENTUAIS
# ==========================================

print("\n--- PERCENTUAIS ---")


percentuais = [
    (
        "UF",
        uf,
        "taxa_alfabetizacao"
    ),
    (
        "Meta Brasil",
        meta_brasil,
        "taxa_alfabetizacao"
    ),
    (
        "Meta UF",
        meta_uf,
        "taxa_alfabetizacao"
    ),
    (
        "Meta Município",
        meta_municipio,
        "taxa_alfabetizacao"
    ),
    (
        "Município",
        municipio,
        "taxa_alfabetizacao"
    )
]


for nome, df, coluna in percentuais:

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
            f"[ATENÇÃO] {nome}: "
            f"{len(invalidos)} valores "
            "fora do intervalo 0-100"
        )


# ==========================================
# RELACIONAMENTOS
# ==========================================

print("\n--- RELACIONAMENTOS ---")


# ------------------------------------------
# META UF -> UF
# ------------------------------------------

ufs_referencia = set(
    uf["sigla_uf"].dropna().unique()
)

ufs_meta = set(
    meta_uf["sigla_uf"].dropna().unique()
)

ufs_sem_correspondencia = sorted(
    ufs_meta - ufs_referencia
)


if len(ufs_sem_correspondencia) == 0:

    print(
        "[OK] Meta UF -> UF: "
        "todas as chaves possuem correspondência"
    )

else:

    print(
        "[ATENÇÃO] Meta UF -> UF: "
        f"{len(ufs_sem_correspondencia)} "
        "chaves sem correspondência"
    )

    print(
        "Siglas sem correspondência:",
        ufs_sem_correspondencia
    )


# ------------------------------------------
# META MUNICÍPIO -> MUNICÍPIO
# ------------------------------------------

ids_municipio = set(
    municipio[
        "id_municipio"
    ].dropna().unique()
)

ids_meta_municipio = set(
    meta_municipio[
        "id_municipio"
    ].dropna().unique()
)

meta_sem_municipio = (
    ids_meta_municipio
    - ids_municipio
)


if len(meta_sem_municipio) == 0:

    print(
        "[OK] Meta Município -> Município: "
        "todas as chaves possuem correspondência"
    )

else:

    print(
        "[ATENÇÃO] Meta Município -> Município: "
        f"{len(meta_sem_municipio)} "
        "chaves sem correspondência"
    )


# ------------------------------------------
# ALUNOS -> MUNICÍPIO
# ------------------------------------------

ids_alunos = set(
    alunos[
        "id_municipio"
    ].dropna().unique()
)

alunos_sem_municipio = (
    ids_alunos
    - ids_municipio
)


if len(alunos_sem_municipio) == 0:

    print(
        "[OK] Alunos -> Município: "
        "todas as chaves possuem correspondência"
    )

else:

    print(
        "[ATENÇÃO] Alunos -> Município: "
        f"{len(alunos_sem_municipio)} "
        "chaves sem correspondência"
    )


# ==========================================
# IBGE
# ==========================================

print("\n--- INTEGRAÇÃO COM IBGE ---")


ids_ibge = set(
    ibge[
        "id_municipio"
    ].dropna().unique()
)


# Municípios educacionais sem IBGE
municipios_sem_ibge = (
    ids_municipio
    - ids_ibge
)


if len(municipios_sem_ibge) == 0:

    print(
        "[OK] Município -> IBGE: "
        "todos os municípios possuem correspondência"
    )

else:

    print(
        "[ATENÇÃO] Município -> IBGE: "
        f"{len(municipios_sem_ibge)} "
        "municípios sem correspondência"
    )


# Meta Município sem IBGE
meta_sem_ibge = (
    ids_meta_municipio
    - ids_ibge
)


if len(meta_sem_ibge) == 0:

    print(
        "[OK] Meta Município -> IBGE: "
        "todas as chaves possuem correspondência"
    )

else:

    print(
        "[ATENÇÃO] Meta Município -> IBGE: "
        f"{len(meta_sem_ibge)} "
        "chaves sem correspondência"
    )


# ==========================================
# NULOS IBGE
# ==========================================

print("\n--- VALORES NULOS IBGE ---")


nulos_ibge = (
    ibge.isnull()
    .sum()
)

nulos_ibge = nulos_ibge[
    nulos_ibge > 0
]


if len(nulos_ibge) == 0:

    print(
        "[OK] IBGE: nenhum valor nulo"
    )

else:

    print(
        "[ATENÇÃO] IBGE possui valores nulos:"
    )

    for coluna, quantidade in nulos_ibge.items():

        print(
            f"  {coluna}: {quantidade}"
        )


# ==========================================
# PROFICIÊNCIA
# ==========================================

print("\n--- PROFICIÊNCIA ---")


ausentes_nulos = alunos[
    (alunos["presenca"] == "Ausente")
    & (alunos["proficiencia"].isna())
]


presentes_nulos = alunos[
    (alunos["presenca"] == "Presente")
    & (alunos["proficiencia"].isna())
]


print(
    "Proficiência nula entre ausentes:",
    len(ausentes_nulos)
)

print(
    "Proficiência nula entre presentes:",
    len(presentes_nulos)
)


# ==========================================
# VALIDAÇÃO DA GOLD ENRIQUECIDA
# ==========================================

print("\n--- GOLD MUNICÍPIO + IBGE ---")


total_gold = len(gold_ibge)

sem_nome = (
    gold_ibge[
        "nome_municipio"
    ].isnull().sum()
)

sem_regiao = (
    gold_ibge[
        "regiao"
    ].isnull().sum()
)


print(
    f"Registros na Gold enriquecida: "
    f"{total_gold}"
)


if sem_nome == 0:

    print(
        "[OK] Gold IBGE: "
        "todos os registros possuem município"
    )

else:

    print(
        f"[ATENÇÃO] Gold IBGE: "
        f"{sem_nome} registros sem município"
    )


if sem_regiao == 0:

    print(
        "[OK] Gold IBGE: "
        "todos os registros possuem região"
    )

else:

    print(
        f"[ATENÇÃO] Gold IBGE: "
        f"{sem_regiao} registros sem região"
    )


# ==========================================
# RESUMO FINAL
# ==========================================

print("\n====================================")
print("VALIDAÇÃO DE QUALIDADE CONCLUÍDA")
print("====================================")