import pandas as pd
import numpy as np

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    fbeta_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)

# ============================================================
# 1. PARÂMETROS DO MLP
# ============================================================

MLP_PARAMS = {
    # Arquitetura da rede
    "hidden_layer_sizes": (64, 32, 16),

    # Função de ativação dos neurônios
    "activation": "relu",

    # Algoritmo de otimização
    "solver": "adam",

    # Taxa de aprendizado inicial
    "learning_rate_init": 0.001,

    # Quantidade máxima de épocas
    "max_iter": 100,

    # Tamanho do lote utilizado no treinamento
    "batch_size": 64,

    # Regularização L2
    "alpha": 0.0001,

    # Para interromper quando não houver melhoria
    "early_stopping": True,

    # Parte do treinamento utilizada para validação
    "validation_fraction": 0.1,

    # Número de épocas sem melhoria antes de parar
    "n_iter_no_change": 10,

    # Reprodutibilidade
    "random_state": 42
}


# ============================================================
# 2. CARREGAMENTO DO DATASET
# ============================================================

arquivo = "tabela_final\part-00000-13fcc452-2493-4299-ab17-d369f64d2ad3-c000.csv"

df = pd.read_csv(arquivo)


# ============================================================
# 3. VARIÁVEL TARGET
# ============================================================

target = "delivered_on_time"


# ============================================================
# 4. REMOÇÃO DE COLUNAS COM POSSÍVEL DATA LEAKAGE
# ============================================================

colunas_remover = [
    target,

    # Datas / timestamps
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",

    # Variáveis calculadas após o processo de entrega
    "shipping_delay",
    "delivery_time",

    # Avaliação posterior à entrega
    "review_score"
]

colunas_remover = [
    coluna for coluna in colunas_remover
    if coluna in df.columns
]


# ============================================================
# 5. SEPARAÇÃO ENTRE X E Y
# ============================================================

X = df.drop(columns=colunas_remover)
y = df[target]


# ============================================================
# 6. CONVERSÃO DE VARIÁVEIS CATEGÓRICAS
# ============================================================

X = pd.get_dummies(
    X,
    drop_first=True
)


# ============================================================
# 7. TRATAMENTO DE VALORES AUSENTES
# ============================================================

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(
    X.median(numeric_only=True)
)

X = X.fillna(0)


# ============================================================
# 8. DIVISÃO TEMPORAL
# ============================================================

data_split = "2018-07-01"

data_coluna = "order_delivered_carrier_date"

df[data_coluna] = pd.to_datetime(
    df[data_coluna],
    errors="coerce"
)

train_mask = df[data_coluna] < data_split
test_mask = df[data_coluna] >= data_split

X_train = X.loc[train_mask]
X_test = X.loc[test_mask]

y_train = y.loc[train_mask]
y_test = y.loc[test_mask]


# ============================================================
# 9. NORMALIZAÇÃO
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)


# ============================================================
# 10. CRIAÇÃO DO MLP
# ============================================================

mlp = MLPClassifier(
    **MLP_PARAMS
)


# ============================================================
# 11. TREINAMENTO
# ============================================================

mlp.fit(
    X_train_scaled,
    y_train
)


# ============================================================
# 12. PREDIÇÃO
# ============================================================

y_pred = mlp.predict(
    X_test_scaled
)

y_prob = mlp.predict_proba(
    X_test_scaled
)[:, 1]


# ============================================================
# 13. MÉTRICAS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    pos_label=0,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    pos_label=0,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    pos_label=0,
    zero_division=0
)

f2 = fbeta_score(
    y_test,
    y_pred,
    beta=2,
    pos_label=0,
    zero_division=0
)

auc = roc_auc_score(
    y_test,
    y_prob
)


# ============================================================
# 14. RESULTADOS
# ============================================================

print("\n" + "=" * 60)
print("RESULTADOS - MLP")
print("=" * 60)

print(f"Arquitetura: {MLP_PARAMS['hidden_layer_sizes']}")
print(f"Activation: {MLP_PARAMS['activation']}")
print(f"Learning rate: {MLP_PARAMS['learning_rate_init']}")
print(f"Batch size: {MLP_PARAMS['batch_size']}")
print(f"Épocas máximas: {MLP_PARAMS['max_iter']}")

print("\nQuantidade de amostras:")
print(f"Treino: {len(X_train)}")
print(f"Teste:  {len(X_test)}")

print("\nMétricas:")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-score:  {f1:.4f}")
print(f"F2-score:  {f2:.4f}")
print(f"ROC-AUC:   {auc:.4f}")

print("\nMatriz de confusão:")
print(confusion_matrix(y_test, y_pred))

print("\nRelatório de classificação:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nQuantidade de épocas executadas:")
print(mlp.n_iter_)