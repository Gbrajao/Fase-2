import pandas as pd
from pathlib import Path


# Arquivo original da camada Bronze
BRONZE_FILE = Path(
    "data/bronze/br_inep_avaliacao_alfabetizacao_uf.csv.gz"
)

# Pasta de destino da camada Silver
SILVER_PATH = Path("data/silver")


def processar_dados_silver():

    print("Iniciando processamento da camada Silver...")

    # 1. Ler os dados brutos
    df = pd.read_csv(
        BRONZE_FILE,
        compression="gzip"
    )

    print(f"Registros recebidos da Bronze: {len(df)}")

    # 2. Remover registros duplicados
    quantidade_antes = len(df)

    df = df.drop_duplicates()

    quantidade_depois = len(df)

    print(
        f"Duplicados removidos: "
        f"{quantidade_antes - quantidade_depois}"
    )

    # 3. Padronizar a sigla da UF
    df["sigla_uf"] = (
        df["sigla_uf"]
        .str.strip()
        .str.upper()
    )

    # 4. Validar taxa de alfabetização
    # Como é percentual, deve estar entre 0 e 100
    taxas_invalidas = df[
        ~df["taxa_alfabetizacao"].between(0, 100)
    ]

    if len(taxas_invalidas) > 0:
        print(
            f"ATENÇÃO: {len(taxas_invalidas)} "
            "taxas de alfabetização inválidas."
        )
    else:
        print("Taxas de alfabetização válidas.")

    # 5. Verificar valores nulos nas proporções
    colunas_niveis = [
        f"proporcao_aluno_nivel_{i}"
        for i in range(9)
    ]

    quantidade_nulos = (
        df[colunas_niveis]
        .isnull()
        .sum()
        .sum()
    )

    print(
        f"Valores nulos nas colunas de nível: "
        f"{quantidade_nulos}"
    )

    # Os valores nulos são preservados.
    # A análise exploratória mostrou que eles pertencem
    # aos registros de 2023 e não devem ser convertidos
    # artificialmente para zero.

    # 6. Criar pasta Silver
    SILVER_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    # 7. Arquivo de saída
    arquivo_saida = (
        SILVER_PATH /
        "avaliacao_alfabetizacao_uf.parquet"
    )

    # 8. Salvar em Parquet
    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print("\nCamada Silver criada com sucesso!")
    print(f"Registros finais: {len(df)}")
    print(f"Arquivo: {arquivo_saida}")


if __name__ == "__main__":
    processar_dados_silver()
    print("\n\n======================================")
print("META ALFABETIZAÇÃO BRASIL")
print("======================================")

ARQUIVO_META_BRASIL = Path(
    "data/bronze/"
    "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_brasil.csv.gz"
)

meta_brasil = pd.read_csv(
    ARQUIVO_META_BRASIL,
    compression="gzip"
)

print("\n--- PRIMEIRAS LINHAS ---")
print(meta_brasil.head())

print("\n--- TAMANHO DA BASE ---")
print(f"Linhas: {meta_brasil.shape[0]}")
print(f"Colunas: {meta_brasil.shape[1]}")

print("\n--- NOMES DAS COLUNAS ---")
print(meta_brasil.columns.tolist())

print("\n--- TIPOS DOS DADOS ---")
print(meta_brasil.dtypes)

print("\n--- VALORES NULOS ---")
print(meta_brasil.isnull().sum())

print("\n--- DADOS COMPLETOS ---")
print(meta_brasil.to_string(index=False))
print("\n\n======================================")
print("META ALFABETIZAÇÃO POR UF")
print("======================================")

ARQUIVO_META_UF = Path(
    "data/bronze/"
    "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_uf.csv.gz"
)

meta_uf = pd.read_csv(
    ARQUIVO_META_UF,
    compression="gzip"
)

print("\n--- PRIMEIRAS LINHAS ---")
print(meta_uf.head())

print("\n--- TAMANHO DA BASE ---")
print(f"Linhas: {meta_uf.shape[0]}")
print(f"Colunas: {meta_uf.shape[1]}")

print("\n--- NOMES DAS COLUNAS ---")
print(meta_uf.columns.tolist())

print("\n--- TIPOS DOS DADOS ---")
print(meta_uf.dtypes)

print("\n--- VALORES NULOS ---")
print(meta_uf.isnull().sum())

print("\n--- DUPLICADOS ---")
print(meta_uf.duplicated().sum())
print("\n\n======================================")
print("META ALFABETIZAÇÃO POR MUNICÍPIO")
print("======================================")

ARQUIVO_META_MUNICIPIO = Path(
    "data/bronze/"
    "br_inep_avaliacao_alfabetizacao_meta_alfabetizacao_municipio.csv.gz"
)

meta_municipio = pd.read_csv(
    ARQUIVO_META_MUNICIPIO,
    compression="gzip"
)

print("\n--- PRIMEIRAS LINHAS ---")
print(meta_municipio.head())

print("\n--- TAMANHO DA BASE ---")
print(f"Linhas: {meta_municipio.shape[0]}")
print(f"Colunas: {meta_municipio.shape[1]}")

print("\n--- NOMES DAS COLUNAS ---")
print(meta_municipio.columns.tolist())

print("\n--- TIPOS DOS DADOS ---")
print(meta_municipio.dtypes)

print("\n--- VALORES NULOS ---")
print(meta_municipio.isnull().sum())

print("\n--- DUPLICADOS ---")
print(meta_municipio.duplicated().sum())
print("\n\n======================================")
print("MUNICÍPIO")
print("======================================")

ARQUIVO_MUNICIPIO = Path(
    "data/bronze/"
    "br_inep_avaliacao_alfabetizacao_municipio.csv.gz"
)

municipio = pd.read_csv(
    ARQUIVO_MUNICIPIO,
    compression="gzip"
)

print("\n--- PRIMEIRAS LINHAS ---")
print(municipio.head())

print("\n--- TAMANHO DA BASE ---")
print(f"Linhas: {municipio.shape[0]}")
print(f"Colunas: {municipio.shape[1]}")

print("\n--- NOMES DAS COLUNAS ---")
print(municipio.columns.tolist())

print("\n--- TIPOS DOS DADOS ---")
print(municipio.dtypes)

print("\n--- VALORES NULOS ---")
print(municipio.isnull().sum())

print("\n--- DUPLICADOS ---")
print(municipio.duplicated().sum())

print("\n--- MUNICÍPIOS ÚNICOS ---")
print(municipio["id_municipio"].nunique())
print("\n\n======================================")
print("ALUNOS - AMOSTRA 2024")
print("======================================")

ARQUIVO_ALUNOS = Path(
    "data/bronze/alunos_2024_amostra.csv"
)

alunos = pd.read_csv(
    ARQUIVO_ALUNOS
)

print("\n--- PRIMEIRAS LINHAS ---")
print(alunos.head())

print("\n--- TAMANHO DA BASE ---")
print(f"Linhas: {alunos.shape[0]}")
print(f"Colunas: {alunos.shape[1]}")

print("\n--- NOMES DAS COLUNAS ---")
print(alunos.columns.tolist())

print("\n--- TIPOS DOS DADOS ---")
print(alunos.dtypes)

print("\n--- VALORES NULOS ---")
print(alunos.isnull().sum())

print("\n--- DUPLICADOS ---")
print(alunos.duplicated().sum())

print("\n--- MUNICÍPIOS ÚNICOS ---")
print(alunos["id_municipio"].nunique())

print("\n--- VALORES DE REDE ---")
print(alunos["rede"].value_counts(dropna=False))

print("\n--- VALORES DE PRESENÇA ---")
print(alunos["presenca"].value_counts(dropna=False))

print("\n--- VALORES DE ALFABETIZADO ---")
print(alunos["alfabetizado"].value_counts(dropna=False))

print("\n--- ESTATÍSTICAS DE PROFICIÊNCIA ---")
print(alunos["proficiencia"].describe())