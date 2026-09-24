# Predict Delivery — Protótipo do TCC

Protótipo completo em **HTML + CSS + JavaScript** com backend em **FastAPI**.

## O que já está implementado

- Tela inicial com formulário corporativo.
- Cálculo automático do volume.
- Dados naturais para o usuário; as features derivadas são calculadas no backend.
- Tela de carregamento.
- Tela de resultado com:
  - classificação atraso / dentro do prazo;
  - probabilidade de atraso;
  - nível de risco;
  - fatores que influenciaram a previsão;
  - comparativo de Deep Learning, Random Forest, XGBoost, Árvore de Decisão e KNN;
  - perfil de cluster (K-Means);
  - identificação de padrão/outlier (DBSCAN);
  - representação 2D inspirada no PCA;
  - resumo das variáveis utilizadas.
- Modo demonstração: funciona mesmo sem backend.

> Importante: o modo demonstração NÃO substitui os modelos treinados no TCC. Ele existe para permitir que o front-end seja testado antes da integração final.

---

## Estrutura

```text
aplicacao-web-tcc/
├─ frontend/
│  ├─ index.html
│  ├─ resultado.html
│  ├─ css/
│  │  └─ style.css
│  └─ js/
│     ├─ form.js
│     └─ resultado.js
├─ backend/
│  └─ app.py
└─ README.md
```

## Atenção acadêmica

Os valores de K-Means, DBSCAN, PCA e do comparativo entre modelos usados no modo demonstração são ilustrativos.
Na versão final do TCC, substitua-os pelos resultados reais produzidos pelos artefatos treinados.

Também vale substituir a lista simplificada de feriados do backend por uma base oficial/arquivo de calendário
igual à utilizada no treinamento do projeto, para garantir consistência entre treino e produção.
