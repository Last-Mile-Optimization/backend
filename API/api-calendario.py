import requests
import pandas as pd

ano = 2026

url = f"https://date.nager.at/api/v3/publicholidays/{ano}/BR"

response = requests.get(url)
response.raise_for_status()

dados = response.json()

df = pd.DataFrame(dados)

df["types"] = df["types"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
df["counties"] = df["counties"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")

df.to_csv(f"feriados_brasil_{ano}.csv", index=False, encoding="utf-8-sig")

print(f"CSV gerado com sucesso: feriados_brasil_{ano}.csv")
print(df.head())