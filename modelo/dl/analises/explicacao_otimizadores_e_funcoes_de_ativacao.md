# ReLU, Adam, tanh e SGD: Conceitos, Vantagens e Comparação

## ReLU (Rectified Linear Unit)

A ReLU (*Rectified Linear Unit*) é uma função de ativação amplamente utilizada em redes neurais profundas.

### Fórmula

\[
f(x) = \max(0, x)
\]

### Funcionamento

- Valores negativos tornam-se 0.
- Valores positivos permanecem inalterados.
- Introduz não-linearidade na rede, permitindo o aprendizado de padrões complexos.

### Vantagens

- Treinamento mais rápido.
- Menor problema de gradientes desaparecendo (*vanishing gradients*).
- Baixo custo computacional.
- Excelente desempenho em redes profundas.

### Desvantagens

- Pode ocorrer o problema dos "neurônios mortos" (*dying ReLU*), quando alguns neurônios passam a produzir apenas zero.
- Não é centrada em zero.

### Quando utilizar

A ReLU costuma ser a escolha padrão para problemas de classificação, regressão e aprendizado profundo devido à sua simplicidade e eficiência.

---

## Adam (Adaptive Moment Estimation)

Adam é um algoritmo de otimização utilizado para atualizar os pesos da rede neural durante o treinamento.

### Funcionamento

O Adam combina conceitos de:

- Gradient Descent
- Momentum
- RMSProp

Ele adapta automaticamente a taxa de aprendizado para cada parâmetro da rede.

### Vantagens

- Convergência rápida.
- Menos sensível à escolha do *learning rate*.
- Funciona muito bem em conjuntos de dados grandes.
- Excelente para redes profundas.
- Reduz oscilações durante o treinamento.

### Desvantagens

- Consome mais memória que SGD.
- Em alguns casos específicos pode produzir soluções menos generalizáveis.

### Quando utilizar

É frequentemente o primeiro otimizador recomendado para novos projetos de Deep Learning.

---

## tanh (Tangente Hiperbólica)

A função de ativação tanh é uma evolução da função sigmoide.

### Fórmula

\[
tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}
\]

### Faixa de saída

\[
[-1, 1]
\]

### Funcionamento

- Valores negativos permanecem negativos.
- Valores positivos permanecem positivos.
- A saída é centrada em zero.

### Vantagens

- Melhor que a Sigmoid em muitos problemas.
- Saída centrada em zero.
- Pode representar naturalmente relações positivas e negativas.

### Desvantagens

- Sofre com o problema do gradiente desaparecendo.
- Pode saturar para valores próximos de -1 e +1.
- Em redes profundas normalmente aprende mais lentamente que ReLU.

### Quando utilizar

Ainda pode ser útil em camadas específicas ou em alguns tipos de redes recorrentes, mas atualmente é menos utilizada em redes profundas tradicionais.

---

## SGD (Stochastic Gradient Descent)

SGD é um dos algoritmos de otimização mais clássicos do aprendizado de máquina.

### Fórmula simplificada

\[
W = W - \eta \nabla J
\]

onde:

- \(W\) representa os pesos;
- \(\eta\) representa a taxa de aprendizado;
- \(\nabla J\) representa o gradiente da função de perda.

### Funcionamento

O SGD atualiza os pesos utilizando amostras individuais ou pequenos lotes de dados (*mini-batches*).

### Vantagens

- Simples de implementar.
- Baixo consumo de memória.
- Em alguns casos produz melhor capacidade de generalização.

### Desvantagens

- Convergência mais lenta.
- Maior sensibilidade ao *learning rate*.
- Pode oscilar bastante durante o treinamento.
- Requer mais ajustes de hiperparâmetros.

### Quando utilizar

É comum em pesquisas acadêmicas e em situações onde o objetivo é maximizar a capacidade de generalização do modelo.

---

# Comparação entre ReLU e tanh

| Característica | ReLU | tanh |
|---------------|-------|-------|
| Faixa de saída | [0, +∞] | [-1, 1] |
| Velocidade de treinamento | Alta | Média |
| Gradiente desaparecendo | Baixa incidência | Alta incidência |
| Redes profundas | Excelente | Limitada |
| Uso atual | Muito frequente | Menos frequente |

### Melhor opção

✅ **ReLU**

Em aplicações modernas de Deep Learning, a ReLU geralmente apresenta treinamento mais rápido e maior estabilidade.

---

# Comparação entre Adam e SGD

| Característica | Adam | SGD |
|---------------|------|------|
| Velocidade de convergência | Alta | Baixa |
| Ajuste automático do learning rate | Sim | Não |
| Facilidade de uso | Alta | Média |
| Sensibilidade aos hiperparâmetros | Baixa | Alta |
| Generalização | Boa | Muito boa em alguns casos |

### Melhor opção

✅ **Adam**

Para a maioria dos projetos, Adam oferece melhores resultados com menos ajustes.

---

# Melhor combinação

## ReLU + Adam

```python
activation = "relu"
solver = "adam"
```

### Vantagens

- Aprendizado mais rápido.
- Menor risco de gradientes desaparecendo.
- Melhor aproveitamento das camadas profundas.
- Convergência mais eficiente.
- Menor necessidade de ajuste fino dos hiperparâmetros.

Essa é atualmente a combinação mais utilizada em problemas de classificação e regressão com redes neurais MLP.

---

## tanh + SGD

```python
activation = "tanh"
solver = "sgd"
```

### Vantagens

- Estrutura mais tradicional.
- Pode apresentar boa generalização em alguns cenários.

### Desvantagens

- Convergência mais lenta.
- Maior chance de ficar presa em platôs.
- Mais sensível à escolha da taxa de aprendizado.
- Pode sofrer com gradientes desaparecendo.

---

# Conclusão

Para o seu experimento, a combinação:

```python
activation = "relu"
solver = "adam"
```

é a mais indicada. Os gráficos mostram que essa configuração conseguiu reduzir continuamente a *loss* durante o treinamento, mantendo uma acurácia de validação elevada e estável.

Já a combinação:

```python
activation = "tanh"
solver = "sgd"
```

atingiu rapidamente um platô de aprendizado e acionou o *Early Stopping* mais cedo, indicando menor eficiência na otimização.

De forma geral, para redes MLP modernas, **ReLU + Adam é considerada a combinação padrão e mais recomendada**, enquanto **tanh + SGD** costuma ser utilizada apenas em casos específicos ou experimentais.