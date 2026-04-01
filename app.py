import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="One-Rule — Doença Cardíaca",
)

# ── Layout ──────────────────────────────────────────────────────────────────

app.layout = dbc.Container(
    fluid=False,
    style={"maxWidth": "680px", "paddingTop": "2rem", "paddingBottom": "3rem"},
    children=[

        html.H1("Previsão de Doença Cardíaca - Algoritmo One-Rule", style={"fontWeight": "500", "fontSize": "1.5rem"}),
        html.P(
            "O atributo com maior peso decide sozinho a classificação de risco cardiovascular.",
            className="text-muted",
            style={"fontSize": "0.875rem", "marginBottom": "1.75rem"},
        ),

        html.Hr(),

        # ── Atributo 1: Dor torácica ─────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Label("Dor torácica", className="fw-medium", style={"fontSize": "0.875rem"}),
                dbc.RadioItems(
                    id="dor",
                    options=[
                        {"label": "Nenhuma", "value": "nenhuma"},
                        {"label": "Atípica", "value": "atipica"},
                        {"label": "Angina típica", "value": "angina"},
                    ],
                    value="nenhuma",
                    inline=True,
                    className="mt-1",
                ),
            ])
        ], className="mb-3"),

        # ── Atributo 2: Idade ────────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Label(
                    ["Idade: ", html.Span(id="idade-label", style={"fontWeight": "500"})],
                    style={"fontSize": "0.875rem"},
                ),
                dcc.Slider(
                    id="idade",
                    min=18, max=90, step=1, value=40,
                    marks={18: "18", 45: "45", 55: "55", 65: "65", 90: "90"},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ])
        ], className="mb-3"),

        # ── Atributo 3: Tabagismo ────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Label("Tabagismo", className="fw-medium", style={"fontSize": "0.875rem"}),
                dbc.RadioItems(
                    id="tabagismo",
                    options=[
                        {"label": "Nunca fumou", "value": "nunca"},
                        {"label": "Ex-fumante", "value": "ex"},
                        {"label": "Fumante atual", "value": "atual"},
                    ],
                    value="nunca",
                    inline=True,
                    className="mt-1",
                ),
            ])
        ], className="mb-3"),

        # ── Atributo 4: Diabetes ─────────────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.Label("Diabetes", className="fw-medium", style={"fontSize": "0.875rem"}),
                dbc.RadioItems(
                    id="diabetes",
                    options=[
                        {"label": "Não", "value": "nao"},
                        {"label": "Sim", "value": "sim"},
                    ],
                    value="nao",
                    inline=True,
                    className="mt-1",
                ),
            ])
        ], className="mb-4"),

        html.Hr(),

        # ── Resultado ────────────────────────────────────────────────────
        html.Div(id="resultado"),
    ],
)


# ── Lógica One-Rule ──────────────────────────────────────────────────────────

def calcular_one_rule(dor, idade, tabagismo, diabetes):
    candidatos = [
        {
            "atributo": "Dor torácica",
            "valor": {"nenhuma": "Nenhuma", "atipica": "Atípica", "angina": "Angina típica"}[dor],
            "score": 3 if dor == "angina" else 1 if dor == "atipica" else 0,
            "alto":  "Angina típica é o preditor mais forte de doença coronariana. ECG e avaliação cardiológica urgentes.",
            "medio": "Dor atípica requer investigação para descartar causa cardíaca.",
            "baixo": "Sinal crítico ausente.",
        },
        {
            "atributo": "Diabetes",
            "valor": "Sim" if diabetes == "sim" else "Não",
            "score": 2 if diabetes == "sim" else 0,
            "alto":  "Diabetes duplica o risco cardiovascular. Controle glicêmico e rastreio cardíaco essenciais.",
            "medio": "",
            "baixo": "Fator metabólico crítico ausente.",
        },
        {
            "atributo": "Tabagismo",
            "valor": {"nunca": "Nunca fumou", "ex": "Ex-fumante", "atual": "Fumante atual"}[tabagismo],
            "score": 2 if tabagismo == "atual" else 1 if tabagismo == "ex" else 0,
            "alto":  "Tabagismo ativo é um dos fatores mais impactantes. Cessação imediata recomendada.",
            "medio": "Risco residual de ex-fumante permanece elevado por anos.",
            "baixo": "Ausência de tabagismo remove fator de risco modificável importante.",
        },
        {
            "atributo": "Idade",
            "valor": f"{idade} anos",
            "score": 2 if idade >= 65 else 1 if idade >= 45 else 0,
            "alto":  "Idade ≥ 65 é fator de risco independente. Rastreio periódico e controle de comorbidades prioritários.",
            "medio": "Faixa etária de risco crescente. Revisão anual dos fatores cardiovasculares é recomendada.",
            "baixo": "Faixa etária de menor incidência cardiovascular.",
        },
    ]

    dominante = max(candidatos, key=lambda x: x["score"])
    return dominante, candidatos


# ── Callbacks ────────────────────────────────────────────────────────────────

@callback(
    Output("idade-label", "children"),
    Input("idade", "value"),
)
def atualizar_label_idade(valor):
    return f"{valor} anos"


@callback(
    Output("resultado", "children"),
    Input("dor", "value"),
    Input("idade", "value"),
    Input("tabagismo", "value"),
    Input("diabetes", "value"),
)
def atualizar_resultado(dor, idade, tabagismo, diabetes):
    dominante, candidatos = calcular_one_rule(dor, idade, tabagismo, diabetes)
    score = dominante["score"]

    if score >= 2:
        nivel = "Alto risco"
        descricao = dominante["alto"]
        cor_fundo = "#FCEBEB"
        cor_borda = "#A32D2D"
        cor_texto = "#791F1F"
        cor_label = "#A32D2D"
    elif score == 1:
        nivel = "Risco moderado"
        descricao = dominante["medio"] or dominante["alto"]
        cor_fundo = "#FAEEDA"
        cor_borda = "#BA7517"
        cor_texto = "#633806"
        cor_label = "#854F0B"
    else:
        nivel = "Baixo risco"
        descricao = dominante["baixo"]
        cor_fundo = "#EAF3DE"
        cor_borda = "#639922"
        cor_texto = "#27500A"
        cor_label = "#3B6D11"

    # Tabela de pesos
    linhas_tabela = []
    for c in sorted(candidatos, key=lambda x: -x["score"]):
        destaque = c["atributo"] == dominante["atributo"]
        linhas_tabela.append(
            html.Tr(
                [
                    html.Td(
                        c["atributo"],
                        style={"fontWeight": "500" if destaque else "400", "fontSize": "0.8125rem"},
                    ),
                    html.Td(c["valor"], style={"fontSize": "0.8125rem", "color": "#555"}),
                    html.Td(
                        c["score"],
                        style={
                            "fontWeight": "500" if destaque else "400",
                            "fontSize": "0.8125rem",
                            "color": cor_label if destaque else "#888",
                            "textAlign": "center",
                        },
                    ),
                    html.Td(
                        "← regra ativa" if destaque else "",
                        style={"fontSize": "0.75rem", "color": cor_label},
                    ),
                ],
                style={"background": cor_fundo if destaque else "transparent"},
            )
        )

    return html.Div([

        # Caixa de regra ativa
        html.Div(
            [
                html.P(
                    "Regra ativa",
                    style={"fontSize": "0.75rem", "color": "#888", "marginBottom": "2px"},
                ),
                html.P(
                    f"{dominante['atributo']} = {dominante['valor']} (peso {score})",
                    style={"fontWeight": "500", "fontSize": "0.9375rem", "marginBottom": "0"},
                ),
            ],
            style={
                "background": "#f5f5f5",
                "borderRadius": "8px",
                "padding": "0.75rem 1rem",
                "marginBottom": "1rem",
            },
        ),

        # Caixa de resultado
        html.Div(
            [
                html.P(nivel, style={"fontWeight": "500", "fontSize": "1.1rem", "color": cor_texto, "marginBottom": "4px"}),
                html.P(descricao, style={"fontSize": "0.875rem", "color": cor_texto, "marginBottom": "0", "lineHeight": "1.6"}),
            ],
            style={
                "background": cor_fundo,
                "border": f"0.5px solid {cor_borda}",
                "borderRadius": "12px",
                "padding": "1rem 1.25rem",
                "marginBottom": "1.25rem",
            },
        ),

        # Tabela de pesos
        html.P("Pesos por atributo", style={"fontSize": "0.8125rem", "fontWeight": "500", "marginBottom": "6px"}),
        dbc.Table(
            [
                html.Thead(html.Tr([
                    html.Th("Atributo", style={"fontSize": "0.75rem", "fontWeight": "500"}),
                    html.Th("Valor", style={"fontSize": "0.75rem", "fontWeight": "500"}),
                    html.Th("Peso", style={"fontSize": "0.75rem", "fontWeight": "500", "textAlign": "center"}),
                    html.Th("", style={"fontSize": "0.75rem"}),
                ])),
                html.Tbody(linhas_tabela),
            ],
            bordered=False,
            hover=True,
            size="sm",
            style={"fontSize": "0.8125rem"},
        ),
    ])


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
