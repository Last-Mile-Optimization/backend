import requests
import csv

latitude = -23.6639
longitude = -46.5383

url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude={latitude}"
    f"&longitude={longitude}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code"
    f"&forecast_days=15"
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

    with open("previsao_15_dias.csv", mode="w", newline="", encoding="utf-8") as arquivo:
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

    print("CSV gerado com sucesso: previsao_15_dias.csv")

    for i in range(len(datas)):
        print(f"{datas[i]} | Máx: {temp_max[i]}°C | Mín: {temp_min[i]}°C | Chuva: {chuva[i]} mm | Código: {codigo_clima[i]}")

except requests.exceptions.RequestException as e:
    print("Erro ao consultar a API:", e)
except KeyError:
    print("Erro ao processar os dados retornados pela API.")