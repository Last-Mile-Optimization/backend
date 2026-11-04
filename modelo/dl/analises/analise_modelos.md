# Resumo dos Resultados dos Modelos MLP

## Visão Geral

Foram avaliadas três configurações de redes neurais MLP utilizando a mesma arquitetura `(64, 32, 16)` e os mesmos parâmetros de treinamento, variando principalmente a função de ativação, o algoritmo de otimização e o limiar (*threshold*) de classificação.

---

## MLP_V1

### Configuração

```python
activation = "relu"
solver = "adam"
threshold = padrão (0.50)
```

### Resultados

| Métrica | Valor |
|----------|----------|
| Accuracy | 0.8774 |
| Precision | 0.0625 |
| Recall | 0.0016 |
| F1-Score | 0.0032 |
| F2-Score | 0.0020 |
| ROC-AUC | 0.4735 |
| Épocas Executadas | 21 |

### Análise

O modelo apresentou a maior acurácia entre os três experimentos, porém essa métrica é enganosa devido ao forte desbalanceamento da base.

A matriz de confusão mostra que o modelo classificou quase todos os registros como pertencentes à classe majoritária, identificando apenas **1 verdadeiro positivo** e deixando de detectar praticamente todos os casos positivos.

```text
[[   1  612]
 [  15 4486]]
```

Apesar da elevada acurácia, o modelo possui capacidade praticamente nula de encontrar eventos positivos, resultando em valores extremamente baixos de Recall e F1-Score.

### Conclusão do MLP_V1

O modelo é inadequado para problemas em que a identificação da classe positiva é importante, pois prioriza excessivamente a classe majoritária.

---

## MLP_V2

### Configuração

```python
activation = "relu"
solver = "adam"
threshold = 0.90
```

### Resultados

| Métrica | Valor |
|----------|----------|
| Accuracy | 0.8604 |
| Precision | 0.1314 |
| Recall | 0.0294 |
| F1-Score | 0.0480 |
| F2-Score | 0.0348 |
| ROC-AUC | 0.4735 |
| Épocas Executadas | 21 |

### Análise

Mantendo a mesma configuração da rede e alterando apenas o limiar de decisão (*threshold*), houve uma redução na acurácia, porém ocorreu uma melhora significativa na detecção de positivos.

A matriz de confusão mostra aumento dos verdadeiros positivos:

```text
[[  18  595]
 [ 119 4382]]
```

Comparado ao MLP_V1:

- Precision dobrou.
- Recall aumentou quase 20 vezes.
- F1-Score aumentou significativamente.

Mesmo assim, os resultados ainda são considerados baixos para a identificação da classe positiva.

### Conclusão do MLP_V2

O ajuste do *threshold* tornou o modelo menos conservador e melhorou sua capacidade de identificar positivos, apresentando desempenho superior ao MLP_V1 em métricas mais relevantes para problemas desbalanceados.

---

## MLP_V3

### Configuração

```python
activation = "tanh"
solver = "sgd"
threshold = 0.90
```

### Resultados

| Métrica | Valor |
|----------|----------|
| Accuracy | 0.8080 |
| Precision | 0.0927 |
| Recall | 0.0685 |
| F1-Score | 0.0788 |
| F2-Score | 0.0723 |
| ROC-AUC | 0.4297 |
| Épocas Executadas | 12 |

### Análise

Este modelo apresentou a menor acurácia geral, porém foi o que mais conseguiu identificar exemplos positivos.

A matriz de confusão mostra:

```text
[[  42  571]
 [ 411 4090]]
```

Comparado aos demais modelos:

- Maior Recall.
- Melhor F1-Score.
- Melhor F2-Score.
- Maior quantidade de verdadeiros positivos identificados.

No entanto, houve um aumento considerável nos falsos positivos e uma redução da acurácia global.

Além disso, o treinamento convergiu mais rapidamente, sendo interrompido após apenas 12 épocas devido ao *Early Stopping*.

### Conclusão do MLP_V3

Apesar da menor acurácia, foi o modelo que apresentou melhor equilíbrio entre precisão e recuperação da classe positiva, tornando-se o mais adequado quando o objetivo principal é detectar eventos positivos.

---

# Comparação Final

| Métrica | MLP_V1 | MLP_V2 | MLP_V3 |
|----------|----------|----------|----------|
| Accuracy | **0.8774** | 0.8604 | 0.8080 |
| Precision | 0.0625 | **0.1314** | 0.0927 |
| Recall | 0.0016 | 0.0294 | **0.0685** |
| F1-Score | 0.0032 | 0.0480 | **0.0788** |
| F2-Score | 0.0020 | 0.0348 | **0.0723** |
| ROC-AUC | **0.4735** | **0.4735** | 0.4297 |
| Épocas | 21 | 21 | 12 |

---

# Conclusão Geral

Os resultados mostram que a **acurácia isoladamente não é uma métrica adequada para avaliar este problema**, pois os dados apresentam forte desbalanceamento entre as classes.

- **MLP_V1** obteve a maior acurácia, mas praticamente ignorou a classe positiva.
- **MLP_V2** melhorou a identificação dos positivos apenas ajustando o limiar de decisão.
- **MLP_V3** apresentou a melhor capacidade de detectar a classe positiva, alcançando os maiores valores de Recall, F1-Score e F2-Score.

Considerando a capacidade de identificar corretamente os casos positivos, o **MLP_V3 apresentou o melhor desempenho geral**, mesmo sacrificando parte da acurácia. Já o **MLP_V1 apresentou o pior desempenho prático**, pois falhou em detectar quase todos os exemplos da classe de interesse.