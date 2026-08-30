import pandas as pd
from pathlib import Path


# ==========================================
# CAMINHOS DO PROJETO
# ==========================================

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")

SILVER_PATH.mkdir(parents=True, exist_ok=True)


# ==========================================
# ARQUIVOS DA CAMADA BRONZE
# ==========================================

ARQUIVO_UF = (
    BRONZE_PATH
    / "br_inep_avaliacao_alfabetizacao_uf.csv.gz"
)

ARQUIVO_META_BRASIL = (
    BRONZE_PATH
    / "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_brasil.csv.gz"
)

ARQUIVO_META_UF = (
    BRONZE_PATH
    / "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_uf.csv.gz"
)

ARQUIVO_META_MUNICIPIO = (
    BRONZE_PATH
    / "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz"
)

ARQUIVO_MUNICIPIO = (
    BRONZE_PATH
    / "br_inep_avaliacao_alfabetizacao_municipio.csv.gz"
)

ARQUIVO_ALUNOS = (
    BRONZE_PATH
    / "alunos_2024_amostra.csv"
)

ARQUIVO_IBGE = (
    BRONZE_PATH
    / "ibge_municipios.csv"
)


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def validar_percentual(df, coluna, nome_tabela):

    valores = df[coluna].dropna()

    invalidos = valores[
        ~valores.between(0, 100)
    ]

    if len(invalidos) > 0:
        print(
            f"[ATENÇÃO] {len(invalidos)} valores inválidos "
            f"em {nome_tabela}.{coluna}"
        )
    else:
        print(
            f"[OK] {coluna} válida em {nome_tabela}"
        )


def mostrar_resumo(df, nome_tabela):

    print(f"Registros: {len(df)}")
    print(f"Colunas: {len(df.columns)}")
    print(
        f"Duplicados: {df.duplicated().sum()}"
    )
    print(
        f"Valores nulos: {df.isnull().sum().sum()}"
    )


# ==========================================
# UF
# ==========================================

def processar_uf():

    print("\n==============================")
    print("PROCESSANDO UF")
    print("==============================")

    df = pd.read_csv(
        ARQUIVO_UF,
        compression="gzip"
    )

    mostrar_resumo(df, "UF")

    df = df.drop_duplicates()

    df["sigla_uf"] = (
        df["sigla_uf"]
        .str.strip()
        .str.upper()
    )

    validar_percentual(
        df,
        "taxa_alfabetizacao",
        "UF"
    )

    arquivo_saida = (
        SILVER_PATH
        / "uf.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(
        f"[OK] Arquivo criado: {arquivo_saida}"
    )


# ==========================================
# META BRASIL
# ==========================================

def processar_meta_brasil():

    print("\n==============================")
    print("PROCESSANDO META BRASIL")
    print("==============================")

    df = pd.read_csv(
        ARQUIVO_META_BRASIL,
        compression="gzip"
    )

    mostrar_resumo(
        df,
        "Meta Brasil"
    )

    df = df.drop_duplicates()

    df["rede"] = (
        df["rede"]
        .str.strip()
    )

    validar_percentual(
        df,
        "taxa_alfabetizacao",
        "Meta Brasil"
    )

    arquivo_saida = (
        SILVER_PATH
        / "meta_brasil.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(
        f"[OK] Arquivo criado: {arquivo_saida}"
    )


# ==========================================
# META UF
# ==========================================

def processar_meta_uf():

    print("\n==============================")
    print("PROCESSANDO META UF")
    print("==============================")

    df = pd.read_csv(
        ARQUIVO_META_UF,
        compression="gzip"
    )

    mostrar_resumo(
        df,
        "Meta UF"
    )

    df = df.drop_duplicates()

    df["sigla_uf"] = (
        df["sigla_uf"]
        .str.strip()
        .str.upper()
    )

    df["rede"] = (
        df["rede"]
        .str.strip()
    )

    validar_percentual(
        df,
        "taxa_alfabetizacao",
        "Meta UF"
    )

    arquivo_saida = (
        SILVER_PATH
        / "meta_uf.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(
        f"[OK] Arquivo criado: {arquivo_saida}"
    )


# ==========================================
# META MUNICÍPIO
# ==========================================

def processar_meta_municipio():

    print("\n==============================")
    print("PROCESSANDO META MUNICÍPIO")
    print("==============================")

    df = pd.read_csv(
        ARQUIVO_META_MUNICIPIO,
        compression="gzip"
    )

    mostrar_resumo(
        df,
        "Meta Município"
    )

    df = df.drop_duplicates()

    df["id_municipio"] = (
        df["id_municipio"]
        .astype(str)
        .str.zfill(7)
    )

    df["rede"] = (
        df["rede"]
        .str.strip()
    )

    validar_percentual(
        df,
        "taxa_alfabetizacao",
        "Meta Município"
    )

    arquivo_saida = (
        SILVER_PATH
        / "meta_municipio.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(
        f"[OK] Arquivo criado: {arquivo_saida}"
    )


# ==========================================
# MUNICÍPIO
# ==========================================

def processar_municipio():

    print("\n==============================")
    print("PROCESSANDO MUNICÍPIO")
    print("==============================")

    df = pd.read_csv(
        ARQUIVO_MUNICIPIO,
        compression="gzip"
    )

    mostrar_resumo(
        df,
        "Município"
    )

    df = df.drop_duplicates()

    df["id_municipio"] = (
        df["id_municipio"]
        .astype(str)
        .str.zfill(7)
    )

    validar_percentual(
        df,
        "taxa_alfabetizacao",
        "Município"
    )

    arquivo_saida = (
        SILVER_PATH
        / "municipio.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(
        f"[OK] Arquivo criado: {arquivo_saida}"
    )


# ==========================================
# ALUNOS
# ==========================================

def processar_alunos():

    print("\n==============================")
    print("PROCESSANDO ALUNOS")
    print("==============================")

    df = pd.read_csv(
        ARQUIVO_ALUNOS
    )

    mostrar_resumo(
        df,
        "Alunos"
    )

    df = df.drop_duplicates()

    df["id_municipio"] = (
        df["id_municipio"]
        .astype(str)
        .str.zfill(7)
    )

    df["municipio"] = (
        df["municipio"]
        .str.strip()
    )

    df["serie"] = (
        df["serie"]
        .str.strip()
    )

    df["rede"] = (
        df["rede"]
        .str.strip()
    )

    df["presenca"] = (
        df["presenca"]
        .str.strip()
    )

    df["alfabetizado"] = (
        df["alfabetizado"]
        .str.strip()
    )

    proficiencias_invalidas = df[
        (df["proficiencia"].notna())
        & (df["proficiencia"] < 0)
    ]

    if len(proficiencias_invalidas) > 0:
        print(
            f"[ATENÇÃO] {len(proficiencias_invalidas)} "
            "proficiências negativas."
        )
    else:
        print(
            "[OK] Proficiências válidas."
        )

    print(
        "Proficiências nulas:",
        df["proficiencia"].isnull().sum()
    )

    arquivo_saida = (
        SILVER_PATH
        / "alunos.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(
        f"[OK] Arquivo criado: {arquivo_saida}"
    )


# ==========================================
# IBGE MUNICÍPIOS
# ==========================================

def processar_ibge():

    print("\n==============================")
    print("PROCESSANDO IBGE MUNICÍPIOS")
    print("==============================")

    df = pd.read_csv(
        ARQUIVO_IBGE,
        dtype={
            "id_municipio": "string"
        }
    )

    mostrar_resumo(
        df,
        "IBGE Municípios"
    )

    df = df.drop_duplicates()

    # O código do município é um identificador,
    # por isso será tratado como texto.
    df["id_municipio"] = (
        df["id_municipio"]
        .str.strip()
        .str.zfill(7)
    )

    df["nome_municipio"] = (
        df["nome_municipio"]
        .str.strip()
    )

    df["sigla_uf"] = (
        df["sigla_uf"]
        .str.strip()
        .str.upper()
    )

    df["nome_uf"] = (
        df["nome_uf"]
        .str.strip()
    )

    df["regiao"] = (
        df["regiao"]
        .str.strip()
    )

    # Validação da chave id_municipio
    ids_nulos = (
        df["id_municipio"]
        .isnull()
        .sum()
    )

    if ids_nulos == 0:
        print(
            "[OK] id_municipio sem valores nulos"
        )
    else:
        print(
            f"[ATENÇÃO] {ids_nulos} IDs nulos"
        )

    ids_duplicados = (
        df["id_municipio"]
        .duplicated()
        .sum()
    )

    if ids_duplicados == 0:
        print(
            "[OK] id_municipio sem duplicidades"
        )
    else:
        print(
            f"[ATENÇÃO] {ids_duplicados} "
            "IDs duplicados"
        )

    print(
        "Valores nulos preservados:",
        df.isnull().sum().sum()
    )

    arquivo_saida = (
        SILVER_PATH
        / "ibge_municipios.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(
        f"[OK] Registros finais: {len(df)}"
    )

    print(
        f"[OK] Arquivo criado: {arquivo_saida}"
    )


# ==========================================
# EXECUÇÃO DA CAMADA SILVER
# ==========================================

print("\nINICIANDO CAMADA SILVER")

processar_uf()
processar_meta_brasil()
processar_meta_uf()
processar_meta_municipio()
processar_municipio()
processar_alunos()
processar_ibge()

print("\n==============================")
print("CAMADA SILVER CONCLUÍDA")
print("==============================")