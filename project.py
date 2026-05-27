from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # salva os gráficos sem precisar abrir janela

import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# CONFIGURAÇÕES
# =========================================================

CSV_PATH = "dados.csv"
# Exemplos:
# CSV_PATH = "PyDatalab/spotify_global_trends.csv"
# CSV_PATH = r"C:\Users\Home\Desktop\workspace\csv\spot.csv"

OUTPUT_DIR = Path("graficos")
OUTPUT_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")


# =========================================================
# LEITURA DOS DADOS
# =========================================================

dados = pd.read_csv(CSV_PATH)

print("Colunas encontradas:")
print(dados.columns)

# Converte streams para número, caso venha como texto
dados["streams"] = pd.to_numeric(
    dados["streams"].astype(str).str.replace(",", "", regex=False),
    errors="coerce"
).fillna(0)


# =========================================================
# FILTROS PADRÕES
# =========================================================

genero_out = [
    "Billboard Hot 100",
    "Offizielle Charts",
    "Dolby Atmos",
    "Special Purpose Artist",
    "Toronto",
    "Girl Group",
    "Falcom"
]

my_genre = [
    "Alternative Rock",
    "Alternative Pop",
    "Indie Pop",
    "Rock",
    "Pop",
    "Hip Hop"
]

my_countries = [
    "US",
    "PR",
    "SE",
    "GB",
    "England",
    "CA",
    "AU",
    "KR",
    "CO",
    "IE",
    "NO"
]


# =========================================================
# FUNÇÃO PARA SALVAR GRÁFICOS
# =========================================================

def salvar_grafico(nome_arquivo):
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / nome_arquivo, dpi=300, bbox_inches="tight")
    plt.close()


# =========================================================
# 1) FLUXO X EVERGREEN POR PAÍS
# =========================================================

table_alta = dados.groupby(["country", "longevity"]).size().unstack(fill_value=0)

if "Evergreen" not in table_alta.columns:
    table_alta["Evergreen"] = 0

table_alta["fluxo"] = table_alta.sum(axis=1)
table_alta["evergreen_ratio"] = table_alta["Evergreen"] / table_alta["fluxo"]
table_alta["evergreen_pct"] = (table_alta["evergreen_ratio"] * 100).round(2)

plot_df = table_alta[table_alta["fluxo"] > 5].copy()

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=plot_df,
    x="fluxo",
    y="evergreen_pct"
)

for country in plot_df.index:
    plt.text(
        plot_df.loc[country, "fluxo"] + 0.3,
        plot_df.loc[country, "evergreen_pct"] + 0.3,
        country
    )

plt.xlabel("Fluxo de músicas")
plt.ylabel("Músicas Evergreen (%)")
plt.title("Fluxo x Permanência por País")
salvar_grafico("01_fluxo_x_evergreen.png")


# =========================================================
# 2) TOP 10 GÊNEROS POR STREAM
# =========================================================

genero_stream = dados.groupby("genre")["streams"].sum()
genero_stream = genero_stream[~genero_stream.index.isin(genero_out)]
genero_stream = genero_stream.sort_values(ascending=False)

top10 = genero_stream.head(10)
top10_milhoes = top10 / 1_000_000

print("\nTOP 10 GÊNEROS POR STREAM:")
print(top10)

plt.figure(figsize=(10, 6))
top10_milhoes.plot(kind="bar")

plt.ylabel("Streams (milhões)")
plt.xlabel("Gêneros")
plt.title("TOP 10 GÊNEROS POR STREAM")
plt.xticks(rotation=45, ha="right")

salvar_grafico("02_top10_generos_stream.png")


# =========================================================
# 3) GÊNEROS EM ALTA
# =========================================================

rising = dados[dados["trend"] == "Rising"]
rising = rising[~rising["genre"].isin(genero_out)]

rising_genero = rising.groupby("genre")["trend"].count()
rising_genero = rising_genero.sort_values(ascending=False)

print("\nGÊNEROS EM ALTA:")
print(rising_genero)

plt.figure(figsize=(10, 6))
rising_genero.plot(kind="bar")

plt.title("GÊNEROS EM ALTA")
plt.ylabel("NÚMERO DE MÚSICAS")
plt.xlabel("GÊNEROS")
plt.xticks(rotation=45, ha="right")

salvar_grafico("03_generos_em_alta.png")


# =========================================================
# 4) GRÁFICO DE PIZZA: LONGEVIDADE DAS MÚSICAS
# =========================================================

longevidade = dados["longevity"].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(
    longevidade,
    labels=longevidade.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("LONGEVIDADE DAS MÚSICAS")

salvar_grafico("04_pizza_longevidade.png")


# =========================================================
# 5) QUANTIDADE DE MÚSICAS POR GÊNERO E PAÍS
# =========================================================

df_filtered = dados[
    dados["genre"].isin(my_genre)
    & dados["country"].isin(my_countries)
]

plt.figure(figsize=(14, 8))

sns.countplot(
    data=df_filtered,
    x="genre",
    hue="country",
    palette="Spectral"
)

start = [1, 2, 3, 4]
fim = list(range(5, 40, 5))
temp = start + fim

plt.yticks(temp)
plt.title(
    "Quantidade de Músicas por Gênero e País",
    fontsize=24,
    fontweight="bold",
    pad=30
)
plt.xlabel("Gênero", fontsize=16, fontweight="bold")
plt.ylabel("Quantidade", fontsize=16, fontweight="bold")
plt.xticks(rotation=45, ha="right")

salvar_grafico("05_quantidade_genero_pais.png")


# =========================================================
# 6) QUANTIDADE DE MÚSICAS POR GÊNERO
# =========================================================

df_generos = dados[dados["genre"].isin(my_genre)]

quantidade = df_generos["genre"].value_counts().reset_index()
quantidade.columns = ["genre", "quantidade"]

plt.figure(figsize=(10, 6))

sns.barplot(
    data=quantidade,
    x="genre",
    y="quantidade"
)

plt.title("Quantidade de Músicas por Gênero", fontsize=14, fontweight="bold")
plt.xlabel("Gênero")
plt.ylabel("Quantidade")
plt.xticks(rotation=45, ha="right")

salvar_grafico("06_quantidade_musicas_genero.png")


# =========================================================
# 7) MÉDIA DE STREAMS POR GÊNERO
# =========================================================

popularidade = (
    df_generos.groupby("genre")["streams"]
    .mean()
    .reset_index()
    .sort_values("streams", ascending=False)
)

popularidade["streams_milhoes"] = popularidade["streams"] / 1_000_000

plt.figure(figsize=(10, 6))

sns.barplot(
    data=popularidade,
    x="genre",
    y="streams_milhoes"
)

plt.title("Média de Streams por Gênero", fontsize=14, fontweight="bold")
plt.xlabel("Gênero")
plt.ylabel("Streams médios (milhões)")
plt.xticks(rotation=45, ha="right")

salvar_grafico("07_media_streams_genero.png")


# =========================================================
# FINAL
# =========================================================

print("\nGráficos gerados com sucesso!")
print(f"Pasta de saída: {OUTPUT_DIR.resolve()}")