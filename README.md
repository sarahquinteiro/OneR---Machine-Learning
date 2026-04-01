# One-Rule — Predição de Doença Cardíaca

Aplicação interativa que utiliza o algoritmo **One-Rule (1R)** para classificar o risco de doença cardíaca com base em 4 atributos clínicos.

## Como funciona

O método One-Rule seleciona o atributo com maior poder preditivo e usa apenas ele para decidir a classificação — sem combinar pontuações, sem caixa-preta. O resultado é totalmente interpretável: você sempre sabe exatamente por que o alerta foi gerado.

```
Usuário preenche os atributos
        ↓
One-Rule identifica o atributo dominante
        ↓
Classificação: Baixo / Moderado / Alto risco
```

## Atributos utilizados

| Atributo | Valores possíveis | Peso máximo |
|---|---|---|
| Dor torácica | Nenhuma / Atípica / Angina típica | 3 |
| Diabetes | Não / Sim | 2 |
| Tabagismo | Nunca fumou / Ex-fumante / Fumante atual | 2 |
| Idade | < 45 / 45–54 / 55–64 / ≥ 65 | 2 |

## Tecnologias

- [Python 3.8+](https://www.python.org/)
- [Dash](https://dash.plotly.com/) — framework para aplicações web interativas em Python
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) — componentes visuais

## Pré-requisitos

- Python 3.8 ou superior
- pip

## Instalação

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/heart-one-rule.git
cd heart-one-rule
```

**2. Crie e ative o ambiente virtual**
```bash
# Criar
python -m venv venv

# Ativar — Windows
venv\Scripts\activate

# Ativar — macOS/Linux
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Rode o app**
```bash
python app.py
```

**5. Acesse no navegador**
```
http://127.0.0.1:8050
```

## Estrutura do projeto

```
heart-one-rule/
├── app.py            # aplicação principal
├── requirements.txt  # dependências
└── README.md         # documentação
```

## Base clínica

Os pesos foram definidos com base nas diretrizes da **American Heart Association (AHA)** e do **American College of Cardiology (ACC)**, que apontam dor torácica típica, diabetes, tabagismo e idade avançada como os principais fatores de risco cardiovascular independentes.

> Este projeto é educacional e não substitui avaliação médica profissional.

## Referências

- Holte, R. C. (1993). *Very simple classification rules perform well on most commonly used datasets*. Machine Learning, 11, 63–91.
- American Heart Association. *2024 Heart Disease and Stroke Statistics*.
- ACC/AHA. *2019 Guideline on the Primary Prevention of Cardiovascular Disease*.
