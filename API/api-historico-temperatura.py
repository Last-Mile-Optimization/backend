import requests
import csv

latitude = -23.6639
longitude = -46.5383
ano = 2016

data_inicio = f"{ano}-01-01"
data_fim = f"{ano}-12-31"

url = (
    f"https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={latitude}"
    f"&longitude={longitude}"
    f"&start_date={data_inicio}"
    f"&end_date={data_fim}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code"
    f"&timezone=auto"
)

try:
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()

    datas = dados["daily"]["time"]
    temp_max = dados["daily"]["temperature_2m_max"]
    temp_min = dados["daily"]["temperature_2m_min"]
    chuva = dados["daily"]["precipitation_sum"]
    codigo_clima = dados["daily"]["weather_code"]

    with open(f"clima_{ano}.csv", mode="w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["Data", "Temperatura Máxima", "Temperatura Mínima", "Chuva (mm)", "Código do Clima"])

        for i in range(len(datas)):
            writer.writerow([
                datas[i],
                temp_max[i],
                temp_min[i],
                chuva[i],
                codigo_clima[i]
            ])

    print(f"CSV gerado com sucesso: clima_{ano}.csv")

except requests.exceptions.RequestException as e:
    print("Erro ao consultar a API:", e)
except KeyError:
    print("Erro ao processar os dados retornados pela API.")