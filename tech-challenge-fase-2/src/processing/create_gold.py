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

ibge = pd.read_parquet(
    SILVER_PATH / "ibge_municipios.parquet"
)

print("[OK] Dados Silver carregados.")


# ==========================================
# FUNÇÃO AUXILIAR
# ==========================================

def obter_meta_ano(linha):

    coluna = f"meta_alfabetizacao_{int(linha['ano'])}"

    if coluna in linha.index:
        return linha[coluna]

    return None


# ==========================================
# GOLD 1 - BRASIL
# RESULTADO X META
# ==========================================

def criar_gold_brasil():

    print("\n==============================")
    print("CRIANDO GOLD BRASIL")
    print("==============================")

    df = meta_brasil.copy()

    df["meta_ano"] = df.apply(
        obter_meta_ano,
        axis=1
    )

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

    df["aluno_presente"] = (
        df["presenca"] == "Presente"
    ).astype(int)

    df["aluno_alfabetizado"] = (
        df["alfabetizado"] == "Sim"
    ).astype(int)

    resumo = (
        df.groupby(
            [
                "ano",
                "id_municipio",
                "municipio"
            ],
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

    resumo[
        "percentual_alfabetizados_amostra"
    ] = (
        resumo["alunos_alfabetizados"]
        / resumo["total_registros_amostra"]
        * 100
    ).round(2)

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

    gold[
        "diferenca_amostra_taxa_oficial"
    ] = (
        gold[
            "percentual_alfabetizados_amostra"
        ]
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
# GOLD 5 - MUNICÍPIO ENRIQUECIDO COM IBGE
# ==========================================

def criar_gold_municipio_ibge():

    print("\n==============================")
    print("CRIANDO GOLD MUNICÍPIO + IBGE")
    print("==============================")

    educacao = meta_municipio.copy()

    # Mantém somente as colunas necessárias do IBGE
    ibge_reduzido = ibge[
        [
            "id_municipio",
            "nome_municipio",
            "sigla_uf",
            "nome_uf",
            "regiao"
        ]
    ].copy()

    # Integra as duas fontes reais
    gold = educacao.merge(
        ibge_reduzido,
        on="id_municipio",
        how="left"
    )

    gold["meta_ano"] = gold.apply(
        obter_meta_ano,
        axis=1
    )

    gold["diferenca_meta"] = (
        gold["taxa_alfabetizacao"]
        - gold["meta_ano"]
    )

    gold["atingiu_meta"] = (
        gold["diferenca_meta"] >= 0
    )

    # Validação simples do enriquecimento
    municipios_sem_ibge = (
        gold["nome_municipio"]
        .isnull()
        .sum()
    )

    print(
        "Registros sem correspondência no IBGE:",
        municipios_sem_ibge
    )

    print(
        "Registros com informação de região:",
        gold["regiao"].notna().sum()
    )

    arquivo_saida = (
        GOLD_PATH
        / "municipio_enriquecido_ibge.parquet"
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
criar_gold_municipio_ibge()

print("\n==============================")
print("CAMADA GOLD CONCLUÍDA")
print("==============================")