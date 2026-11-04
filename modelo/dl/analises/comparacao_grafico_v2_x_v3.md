## 6. O que os gráficos sugerem

A **Imagem 01** mostra uma rede que ainda está aprendendo de forma eficiente:

- *Loss* em queda contínua;
- Acurácia de validação estável em torno de 95%;
- Treinamento consistente e sem sinais claros de estagnação;
- O modelo continua encontrando ajustes que reduzem o erro ao longo das épocas.

Por outro lado, a **Imagem 02** indica que a rede atingiu rapidamente um platô de aprendizado:

- *Loss* apresenta uma queda acentuada apenas nas primeiras épocas;
- Acurácia de validação permanece praticamente constante em 95%;
- As melhorias tornam-se muito pequenas após as primeiras iterações;
- O mecanismo de *Early Stopping* é acionado mais cedo devido à ausência de ganho significativo na validação.

---

## Conclusão

A principal razão para a diferença observada entre os gráficos está na combinação dos parâmetros utilizados:

### Imagem 01

```python
activation = "relu"
solver = "adam"
```

### Imagem 02

```python
activation = "tanh"
solver = "sgd"
```

A combinação **ReLU + Adam** proporciona gradientes mais eficientes e um processo de otimização adaptativo, permitindo que o modelo continue reduzindo a função de perda ao longo de várias épocas. Como resultado, o treinamento apresenta uma convergência mais gradual e consistente.

Já a combinação **tanh + SGD** tende a sofrer mais com problemas de saturação da função de ativação e com atualizações menos eficientes dos pesos. Isso faz com que o modelo alcance rapidamente um platô de aprendizado, reduzindo pouco a perda após as primeiras épocas e acionando o *Early Stopping* antecipadamente.

Embora ambos os modelos tenham alcançado uma acurácia de validação muito próxima de **95%**, o modelo da Imagem 01 demonstra um processo de treinamento mais eficiente e com melhor capacidade de refinamento dos pesos, evidenciado pela redução contínua da *loss* ao longo do treinamento.