# Guia do Notebook ArvoreDeDecisao.ipynb

Este README explica, em linguagem simples, o passo a passo do notebook e o significado de cada parte do codigo.

## 1) Objetivo do notebook

O objetivo do modelo e prever a variavel:
- delivered_on_time

Em outras palavras, o modelo tenta responder se a entrega chegou no prazo (classe 1) ou fora do prazo (classe 0).

## 2) Fluxo geral do notebook

O notebook esta organizado em blocos:

1. Importacao de bibliotecas
2. Leitura e limpeza inicial dos dados
3. Separacao de variaveis de entrada (X) e alvo (y)
4. Treino de uma arvore de decisao basica
5. Avaliacao basica com matriz de confusao e metricas
6. Visualizacao 2D da fronteira de decisao
7. Modelo melhorado com pipeline e validacao cruzada
8. Diagnostico de overfitting
9. Rodada 2 com foco em reduzir overfitting e melhorar classe minoritaria

## 3) Explicacao passo a passo

### Etapa A - Importacao de bibliotecas

Bibliotecas principais:
- pandas: leitura e manipulacao de dados tabulares
- numpy: operacoes numericas
- matplotlib: graficos
- scikit-learn: treinamento e avaliacao do modelo

### Etapa B - Leitura e limpeza do dataset

O codigo:
- le um CSV com os dados processados
- remove colunas que nao serao usadas
- salva em novo arquivo para facilitar os proximos passos

Significado de drop(columns=[...]):
- remove colunas do DataFrame
- evita usar atributos indesejados ou com risco de vazamento de informacao

### Etapa C - Definicao de X e y

- X: todas as colunas de entrada
- y: coluna alvo delivered_on_time

Isso e fundamental para aprendizado supervisionado.

### Etapa D - Divisao treino e teste

train_test_split separa os dados em:
- treino: usado para aprender padroes
- teste: usado para validar se o modelo generaliza

No modelo melhorado, a divisao e estratificada para manter proporcao das classes.

### Etapa E - Treino da arvore de decisao

DecisionTreeClassifier cria regras do tipo:
- se feature A <= valor, vai para um ramo
- senao, vai para outro ramo

No final, cada folha decide a classe prevista.

### Etapa F - Predicao e avaliacao basica

Sao calculadas metricas como:
- Accuracy
- Precision
- Recall
- F1-Score
- Matriz de Confusao

#### Significado da matriz de confusao

Para classificacao binaria:
- Verdadeiro Negativo (TN): classe 0 prevista como 0
- Falso Positivo (FP): classe 0 prevista como 1
- Falso Negativo (FN): classe 1 prevista como 0
- Verdadeiro Positivo (TP): classe 1 prevista como 1

### Etapa G - Propriedades do classificador

Saidas como:
- predict_proba: probabilidade por classe
- classes_: classes aprendidas
- feature_importances_: importancia relativa de cada atributo
- n_features_in_: quantidade de variaveis usadas

### Etapa H - Visualizacao 2D

As secoes de visualizacao usam apenas:
- price
- freight_value

Isso serve para interpretacao visual da fronteira de decisao. E um recorte didatico, nao representa todo o modelo com todas as features.

### Etapa I - Modelo melhorado

Neste bloco, o notebook aplica boas praticas:

1. Preprocessamento com Pipeline
- imputacao de nulos em numericas e categoricas
- OneHotEncoder para variaveis categoricas

2. Busca de hiperparametros com GridSearchCV
- testa varias combinacoes de configuracao da arvore
- escolhe a melhor conforme metrica definida

3. Validacao cruzada estratificada
- mede estabilidade das metricas em diferentes particoes

4. Avaliacoes extras
- classification_report
- matriz normalizada
- ROC-AUC e PR-AUC (quando binario)
- ranking das 15 features mais importantes

### Etapa J - Diagnostico de overfitting

Compara desempenho em treino e teste.

Se treino for muito maior que teste, ha sinal de overfitting.
Exemplo:
- treino perto de 1.00
- teste bem menor

### Etapa K - Rodada 2 (reducao de overfitting)

Melhorias aplicadas:
- arvore mais conservadora (max_depth menor, min_samples maiores, poda com ccp_alpha)
- otimizacao por f1_macro para tratar melhor desbalanceamento
- ajuste de limiar de decisao usando validacao interna

Objetivo:
- diminuir sobreajuste
- melhorar desempenho da classe minoritaria

## 4) Significado das metricas principais

### Accuracy
Proporcao total de acertos.
Pode enganar em base desbalanceada.

### Precision
Entre as previsoes positivas, quantas estavam corretas.

### Recall
Entre os positivos reais, quantos o modelo encontrou.

### F1-Score
Media harmonica entre Precision e Recall.
Boa metrica quando ha desbalanceamento.

### F1 macro
Calcula F1 por classe e tira media simples.
Da peso igual para classe majoritaria e minoritaria.

### F1 weighted
Media ponderada pelo suporte de cada classe.
Favorece a classe com mais exemplos.

### ROC-AUC
Capacidade de separar classes em varios limiares.
Quanto mais perto de 1, melhor.

### PR-AUC
Muito util em base desbalanceada.
Mede relacao entre precisao e revocacao em varios limiares.

## 5) Sobre desbalanceamento de classes

Quando uma classe domina o dataset:
- accuracy e metricas weighted podem parecer altas
- a classe minoritaria pode continuar com desempenho fraco

Por isso e importante olhar:
- macro avg
- recall e F1 da classe minoritaria
- matriz de confusao

## 6) Como interpretar os resultados deste notebook

1. Se o gap treino-teste for grande, suspeite de overfitting.
2. Se classe 0 tiver recall baixo, o modelo ainda perde muitos casos dessa classe.
3. Se a rodada 2 reduzir gap, houve ganho de generalizacao.
4. Nem sempre a melhor accuracy e o melhor modelo de negocio.

## 7) Proximos passos recomendados

1. Testar tecnicas de balanceamento no treino (ex.: SMOTE).
2. Comparar com outros modelos (Random Forest, XGBoost, Logistic Regression).
3. Avaliar metricas orientadas ao negocio (custo de falso positivo vs falso negativo).
4. Salvar o melhor pipeline com versao dos dados e hiperparametros.

## 8) Arquivo principal

Notebook analisado:
- ArvoreDeDecisao.ipynb
