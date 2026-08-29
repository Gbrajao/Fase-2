import pandas as pd
from pathlib import Path


# ==========================================
# CAMINHOS
# ==========================================

SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")

GOLD_PATH.mkdir(parents=True, exist_ok=True)


# ==========================================
# LEITURA DA SILVER
# ==========================================

print("\nLendo dados da camada Silver...")

meta_brasil = pd.read_parquet(
    SILVER_PATH / "meta_brasil.parquet"
)

meta_uf = pd.read_parquet(
    SILVER_PATH / "meta_uf.parquet"
)

meta_municipio = pd.read_parquet(
    SILVER_PATH / "meta_municipio.parquet"
)

alunos = pd.read_parquet(
    SILVER_PATH / "alunos.parquet"
)

print("[OK] Dados Silver carregados.")


# ==========================================
# GOLD 1 - BRASIL
# RESULTADO X META
# ==========================================

def criar_gold_brasil():

    print("\n==============================")
    print("CRIANDO GOLD BRASIL")
    print("==============================")

    df = meta_brasil.copy()

    # Função para buscar a meta correspondente
    # ao próprio ano do registro
    def obter_meta_ano(linha):

        coluna = f"meta_alfabetizacao_{int(linha['ano'])}"

        if coluna in linha.index:
            return linha[coluna]

        return None

    df["meta_ano"] = df.apply(
        obter_meta_ano,
        axis=1
    )

    # Diferença entre resultado e meta
    df["diferenca_meta"] = (
        df["taxa_alfabetizacao"]
        - df["meta_ano"]
    )

    arquivo_saida = (
        GOLD_PATH
        / "resultado_meta_brasil.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(f"[OK] Registros: {len(df)}")
    print(f"[OK] Arquivo: {arquivo_saida}")


# ==========================================
# GOLD 2 - UF
# RESULTADO X META POR ESTADO
# ==========================================

def criar_gold_uf():

    print("\n==============================")
    print("CRIANDO GOLD UF")
    print("==============================")

    df = meta_uf.copy()

    def obter_meta_ano(linha):

        coluna = f"meta_alfabetizacao_{int(linha['ano'])}"

        if coluna in linha.index:
            return linha[coluna]

        return None

    df["meta_ano"] = df.apply(
        obter_meta_ano,
        axis=1
    )

    df["diferenca_meta"] = (
        df["taxa_alfabetizacao"]
        - df["meta_ano"]
    )

    # Indica se atingiu a meta
    df["atingiu_meta"] = (
        df["diferenca_meta"] >= 0
    )

    arquivo_saida = (
        GOLD_PATH
        / "resultado_meta_uf.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(f"[OK] Registros: {len(df)}")
    print(f"[OK] Arquivo: {arquivo_saida}")


# ==========================================
# GOLD 3 - MUNICÍPIO
# RESULTADO X META
# ==========================================

def criar_gold_municipio():

    print("\n==============================")
    print("CRIANDO GOLD MUNICÍPIO")
    print("==============================")

    df = meta_municipio.copy()

    def obter_meta_ano(linha):

        coluna = f"meta_alfabetizacao_{int(linha['ano'])}"

        if coluna in linha.index:
            return linha[coluna]

        return None

    df["meta_ano"] = df.apply(
        obter_meta_ano,
        axis=1
    )

    df["diferenca_meta"] = (
        df["taxa_alfabetizacao"]
        - df["meta_ano"]
    )

    df["atingiu_meta"] = (
        df["diferenca_meta"] >= 0
    )

    arquivo_saida = (
        GOLD_PATH
        / "resultado_meta_municipio.parquet"
    )

    df.to_parquet(
        arquivo_saida,
        index=False
    )

    print(f"[OK] Registros: {len(df)}")
    print(f"[OK] Arquivo: {arquivo_saida}")


# ==========================================
# GOLD 4 - ALUNOS POR MUNICÍPIO
# ==========================================

def criar_gold_alunos_municipio():

    print("\n==============================")
    print("CRIANDO GOLD ALUNOS/MUNICÍPIO")
    print("==============================")

    df = alunos.copy()

    # Colunas auxiliares
    df["aluno_presente"] = (
        df["presenca"] == "Presente"
    ).astype(int)

    df["aluno_alfabetizado"] = (
        df["alfabetizado"] == "Sim"
    ).astype(int)

    # Agrega os alunos por município e ano
    resumo = (
        df.groupby(
            ["ano", "id_municipio", "municipio"],
            as_index=False
        )
        .agg(
            total_registros_amostra=(
                "id_aluno",
                "count"
            ),
            alunos_presentes=(
                "aluno_presente",
                "sum"
            ),
            alunos_alfabetizados=(
                "aluno_alfabetizado",
                "sum"
            ),
            proficiencia_media=(
                "proficiencia",
                "mean"
            )
        )
    )

    # Percentual observado dentro da amostra
    resumo["percentual_alfabetizados_amostra"] = (
        resumo["alunos_alfabetizados"]
        / resumo["total_registros_amostra"]
        * 100
    ).round(2)

    # ======================================
    # INTEGRAÇÃO COM META MUNICIPAL
    # ======================================

    metas = meta_municipio[
        [
            "ano",
            "id_municipio",
            "taxa_alfabetizacao",
            "meta_alfabetizacao_2024",
            "nivel_alfabetizacao",
            "percentual_participacao"
        ]
    ].copy()

    gold = resumo.merge(
        metas,
        on=[
            "ano",
            "id_municipio"
        ],
        how="left"
    )

    # Diferença entre o percentual observado
    # na amostra e a taxa oficial municipal
    gold["diferenca_amostra_taxa_oficial"] = (
        gold["percentual_alfabetizados_amostra"]
        - gold["taxa_alfabetizacao"]
    )

    arquivo_saida = (
        GOLD_PATH
        / "alunos_municipio_analitico.parquet"
    )

    gold.to_parquet(
        arquivo_saida,
        index=False
    )

    print(f"[OK] Registros: {len(gold)}")
    print(f"[OK] Arquivo: {arquivo_saida}")


# ==========================================
# EXECUÇÃO
# ==========================================

print("\nINICIANDO CAMADA GOLD")

criar_gold_brasil()
criar_gold_uf()
criar_gold_municipio()
criar_gold_alunos_municipio()

print("\n==============================")
print("CAMADA GOLD CONCLUÍDA")
print("==============================")