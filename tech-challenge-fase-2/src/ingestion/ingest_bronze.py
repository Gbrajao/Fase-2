import pandas as pd
from pathlib import Path


# Caminho onde os dados Bronze serão salvos
BRONZE_PATH = Path("data/bronze")


def salvar_dados_bronze():
    """
    Cria um exemplo simples de dados e salva
    na camada Bronze.
    """

    # Cria a pasta Bronze caso ela não exista
    BRONZE_PATH.mkdir(parents=True, exist_ok=True)

    # Dados de exemplo
    dados = {
        "municipio": [
            "São Paulo",
            "Rio de Janeiro",
            "Belo Horizonte"
        ],
        "uf": [
            "SP",
            "RJ",
            "MG"
        ],
        "indicador_alfabetizacao": [
            56.2,
            52.8,
            61.5
        ]
    }

    # Transforma os dados em uma tabela
    df = pd.DataFrame(dados)

    # Salva os dados na camada Bronze
    arquivo_saida = BRONZE_PATH / "alfabetizacao_bronze.csv"

    df.to_csv(
        arquivo_saida,
        index=False
    )

    print("Dados salvos com sucesso!")
    print(f"Arquivo criado: {arquivo_saida}")


if __name__ == "__main__":
    salvar_dados_bronze()