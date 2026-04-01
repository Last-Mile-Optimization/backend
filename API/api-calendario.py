import requests
import pandas as pd

url = "https://date.nager.at/api/v3/publicholidays/2026/BR"

response = requests.get(url)
response.raise_for_status()

dados = response.json()

df = pd.DataFrame(dados)

df["types"] = df["types"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
df["counties"] = df["counties"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")

df.to_csv("feriados_brasil_2026.csv", index=False, encoding="utf-8-sig")

print("CSV gerado com sucesso: feriados_brasil_2026.csv")
print(df.head())