import pandas as pd

# 1. Ler o arquivo do HidroWeb (pular metadados, separador ;, encoding latin1)
df = pd.read_csv(
    "../dataset/14990000_Cotas.csv",
    sep=";",
    skiprows=13,
    encoding="latin1"
)

# 2. Manter só os dados consistidos (revisados). Nivel 2 = Consistido.
df = df[df["NivelConsistencia"] == 2]
print("Linhas apos filtrar consistidos:", df.shape[0])

# 3. Converter a coluna Data para tipo data de verdade
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

# 4. Selecionar a data e as 31 colunas de cota diaria
colunas_cota = [f"Cota{d:02d}" for d in range(1, 32)]
df_cotas = df[["Data"] + colunas_cota]

# 5. MELT: transformar as 31 colunas de dia em linhas (de largo para longo)
df_long = df_cotas.melt(
    id_vars=["Data"],
    value_vars=colunas_cota,
    var_name="dia_col",
    value_name="cota"
)
# 6. Corrigir a data: extrair o número do dia de "dia_col" e montar a data real
df_long["dia"] = df_long["dia_col"].str.replace("Cota", "").astype(int)
df_long["data_real"] = pd.to_datetime(
    df_long["Data"].dt.strftime("%Y-%m-") + df_long["dia"].astype(str),
    format="%Y-%m-%d",
    errors="coerce"
)

# 7. Remover linhas invalidas (ex: dia 31 em meses que nao tem, viram NaT)
df_long = df_long.dropna(subset=["data_real", "cota"])

# 8. Calcular a semana epidemiologica (mesmo formato AAAASS da dengue)
iso = df_long["data_real"].dt.isocalendar()
df_long["SE"] = iso["year"] * 100 + iso["week"]

# 9. Agregar: cota media por semana
rio_semanal = df_long.groupby("SE")["cota"].mean().reset_index()
rio_semanal = rio_semanal.rename(columns={"cota": "cota_rio"})

print("Semanas de cota do rio:", rio_semanal.shape[0])
print(rio_semanal.head())

# 10. Salvar o resultado limpo
rio_semanal.to_csv("../dataset/rio_manaus_semanal.csv", index=False)
print("Arquivo rio_manaus_semanal.csv salvo!")