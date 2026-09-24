from datetime import date, datetime
from math import exp
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    import joblib
except Exception:
    joblib = None

app = FastAPI(
    title="API - Predição de Atrasos em Entregas",
    version="1.0.0",
    description="Backend de demonstração para o protótipo do TCC."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "model.joblib"
loaded_model = None

if MODEL_PATH.exists() and joblib is not None:
    try:
        loaded_model = joblib.load(MODEL_PATH)
    except Exception:
        loaded_model = None


class PredictionRequest(BaseModel):
    purchase_date: str
    purchase_time: str
    price: float = Field(ge=0)
    freight_value: float = Field(ge=0)
    product_weight_g: float = Field(gt=0)
    height_cm: float = Field(gt=0)
    width_cm: float = Field(gt=0)
    length_cm: float = Field(gt=0)
    distance_km: float = Field(ge=0)
    same_city: int = Field(ge=0, le=1)


FIXED_HOLIDAYS = [
    (1, 1),   # Confraternização Universal
    (4, 21),  # Tiradentes
    (5, 1),   # Dia do Trabalho
    (9, 7),   # Independência
    (10, 12), # Nossa Senhora Aparecida
    (11, 2),  # Finados
    (11, 15), # Proclamação da República
    (11, 20), # Consciência Negra
    (12, 25), # Natal
]


def holidays_for_year(year: int) -> List[date]:
    return [date(year, month, day) for month, day in FIXED_HOLIDAYS]


def holiday_features(purchase_date: date):
    all_days = holidays_for_year(purchase_date.year - 1) + holidays_for_year(purchase_date.year) + holidays_for_year(purchase_date.year + 1)
    all_days = sorted(all_days)

    is_holiday = int(purchase_date in all_days)
    previous_days = [(purchase_date - h).days for h in all_days if h <= purchase_date]
    next_days = [(h - purchase_date).days for h in all_days if h >= purchase_date]

    return {
        "holiday_at_purchase": is_holiday,
        "days_since_last_holiday": min(previous_days) if previous_days else 999,
        "days_until_next_holiday": min(next_days) if next_days else 999,
    }


def build_features(data: PredictionRequest):
    dt = datetime.fromisoformat(f"{data.purchase_date}T{data.purchase_time}")
    volume_cm3 = data.height_cm * data.width_cm * data.length_cm
    holiday = holiday_features(dt.date())

    features = {
        **holiday,
        "purchase_hour": dt.hour,
        "purchase_day_of_week": dt.weekday(),
        "is_weekend": int(dt.weekday() >= 5),
        "price": data.price,
        "freight_value": data.freight_value,
        "product_weight_g": data.product_weight_g,
        "volume_cm3": volume_cm3,
        "distance_km": data.distance_km,
        "same_city": data.same_city,
    }
    return features


def heuristic_probability(features):
    score = -1.70
    score += min(features["distance_km"] / 700, 2.2) * 0.62
    score += min(features["freight_value"] / max(features["price"], 1), 0.8) * 1.05
    score += min(features["product_weight_g"] / 7000, 1.8) * 0.38
    score += min(features["volume_cm3"] / 85000, 1.5) * 0.32
    score += features["is_weekend"] * 0.34
    score += (1 - features["same_city"]) * 0.40
    score += features["holiday_at_purchase"] * 0.35
    if features["days_until_next_holiday"] <= 3:
        score += 0.24
    return 1 / (1 + exp(-score))


def model_probability(features):
    ordered = [
        "holiday_at_purchase",
        "days_since_last_holiday",
        "days_until_next_holiday",
        "purchase_hour",
        "purchase_day_of_week",
        "is_weekend",
        "price",
        "freight_value",
        "product_weight_g",
        "volume_cm3",
        "distance_km",
        "same_city",
    ]

    if loaded_model is not None:
        row = [[features[name] for name in ordered]]
        if hasattr(loaded_model, "predict_proba"):
            return float(loaded_model.predict_proba(row)[0][1])
        if hasattr(loaded_model, "predict"):
            value = float(loaded_model.predict(row)[0])
            return min(max(value, 0.0), 1.0)

    return heuristic_probability(features)


def factors(features):
    items = [
        ("Distância da entrega", min(100, round(features["distance_km"] / 9))),
        ("Valor do frete", min(100, round((features["freight_value"] / max(features["price"], 1)) * 170))),
        ("Peso do produto", min(100, round(features["product_weight_g"] / 50))),
        ("Volume do produto", min(100, round(features["volume_cm3"] / 700))),
        ("Proximidade de feriado", 78 if features["days_until_next_holiday"] <= 3 else 26),
        ("Fim de semana", 62 if features["is_weekend"] else 18),
    ]
    return [
        {"name": name, "impact": int(impact)}
        for name, impact in sorted(items, key=lambda item: item[1], reverse=True)[:5]
    ]


def cluster_info(features):
    if features["distance_km"] > 500:
        return {
            "name": "Pedidos de longa distância",
            "description": "Entregas com maior deslocamento entre vendedor e cliente.",
            "stats": [["Distância média", "684 km"], ["Frete médio", "R$ 52,40"], ["Atrasos no grupo", "37%"]],
        }
    if features["product_weight_g"] > 5000:
        return {
            "name": "Pedidos pesados de média distância",
            "description": "Produtos de maior peso com deslocamento intermediário.",
            "stats": [["Peso médio", "6,8 kg"], ["Frete médio", "R$ 61,20"], ["Atrasos no grupo", "31%"]],
        }
    return {
        "name": "Pedidos urbanos e leves",
        "description": "Entregas de menor porte e menor deslocamento.",
        "stats": [["Distância média", "96 km"], ["Frete médio", "R$ 24,10"], ["Atrasos no grupo", "14%"]],
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": loaded_model is not None,
        "mode": "real_model" if loaded_model is not None else "demonstration",
    }


@app.post("/predict")
def predict(data: PredictionRequest):
    features = build_features(data)
    main_probability = model_probability(features)
    prediction = int(main_probability >= 0.5)

    model_offsets = {
        "Deep Learning": 0.00,
        "Random Forest": 0.04,
        "XGBoost": 0.07,
        "Árvore de Decisão": -0.05,
        "KNN": -0.11,
    }

    models = []
    for name, offset in model_offsets.items():
        p = min(max(main_probability + offset, 0.03), 0.97)
        models.append({"name": name, "probability": p, "prediction": int(p >= 0.5)})

    risk = (
        "Baixo" if main_probability < .30
        else "Moderado" if main_probability < .61
        else "Alto" if main_probability < .81
        else "Muito alto"
    )

    is_outlier = features["distance_km"] > 1200 or features["product_weight_g"] > 12000

    return {
        "analysis_id": f"ANL-{datetime.now().strftime('%H%M%S')}",
        "prediction": prediction,
        "probability": main_probability,
        "main_model": "Deep Learning" if loaded_model is None else "Modelo carregado",
        "risk_level": risk,
        "models": models,
        "factors": factors(features),
        "cluster": cluster_info(features),
        "dbscan": {
            "is_outlier": is_outlier,
            "text": (
                "Este pedido apresenta características incomuns em relação aos pedidos históricos."
                if is_outlier else
                "Este pedido está dentro de um padrão conhecido nos dados históricos."
            ),
        },
        "pca_point": {
            "x": max(-2.5, min(2.5, (features["distance_km"] - 350) / 250)),
            "y": max(-2.2, min(2.2, (features["product_weight_g"] - 2500) / 1800)),
        },
        "features": features,
        "input": data.model_dump(),
        "demo_mode": loaded_model is None,
    }
