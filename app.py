import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Cargar los datos desde el archivo Excel
file_path = "universidad_data.xlsx"
datos = pd.read_excel(file_path, sheet_name="data_universidad")

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Visualización de Notas Promedio - UNSCH 2024-I"

# Estilos personalizados para las pestañas
tab_styles = {
    "default": {
        "backgroundColor": "#333333",
        "color": "white",
        "border": "1px solid #444444",
        "padding": "10px",
        "fontWeight": "bold",
    },
    "selected": {
        "backgroundColor": "#0056b3",  # Azul más claro
        "color": "white",
        "padding": "10px",
        "fontWeight": "bold",
        "border": "1px solid #0056b3",
    },
}

# Layout de la aplicación
app.layout = dbc.Container([
    html.Div([
        html.H1("Visualización de Notas Promedio - UNSCH 2024-I", className="text-center mb-4"),
        html.H5("Autor: HASBLab Laboratorio de Investición Económica y Social", className="text-center text-muted mb-4"),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Filtros", className="text-light"),
                html.P("Seleccione los géneros que desea incluir en el análisis:", className="text-light"),
                dcc.Checklist(
                    id="generos",
                    options=[
                        {"label": "Varones", "value": "MASCULINO"},
                        {"label": "Mujeres", "value": "FEMENINO"}
                    ],
                    value=["MASCULINO", "FEMENINO"],
                    inputStyle={"margin-right": "10px", "margin-bottom": "5px"},
                    style={"color": "white", "margin-bottom": "15px"}
                ),
                html.P("HASBLab", className="text-muted mt-5"),
            ], className="bg-secondary p-3 rounded"),
        ], width=3),
        dbc.Col([
            dcc.Tabs([
                dcc.Tab(
                    label="Por Escuela",
                    children=[dcc.Graph(id="grafico_escuela", style={"height": "700px"})],
                    style=tab_styles["default"],
                    selected_style=tab_styles["selected"]
                ),
                dcc.Tab(
                    label="Por Lugar de Procedencia",
                    children=[dcc.Graph(id="grafico_procedencia", style={"height": "700px"})],
                    style=tab_styles["default"],
                    selected_style=tab_styles["selected"]
                ),
                dcc.Tab(
                    label="Por Facultad",
                    children=[dcc.Graph(id="grafico_facultad", style={"height": "700px"})],
                    style=tab_styles["default"],
                    selected_style=tab_styles["selected"]
                ),
                dcc.Tab(
                    label="Tabla Resumen",
                    children=[html.Div(id="tabla_resumen", className="table-responsive mt-3")],
                    style=tab_styles["default"],
                    selected_style=tab_styles["selected"]
                ),
            ])
        ], width=9)
    ])
], fluid=True)

# Callbacks para actualizar gráficos y tabla
@app.callback(
    Output("grafico_escuela", "figure"),
    Output("grafico_procedencia", "figure"),
    Output("grafico_facultad", "figure"),
    Output("tabla_resumen", "children"),
    Input("generos", "value")
)
def actualizar_contenido(generos_seleccionados):
    # Filtrar datos
    datos_filtrados = datos[datos["sexo"].isin(generos_seleccionados)]

    # Cálculo del promedio general basado en los datos filtrados
    promedio_general = datos_filtrados["nota_promedio"].mean()

    # Gráfico por Escuela
    df_escuela = datos_filtrados.groupby("escuela_profesional", as_index=False).agg({"nota_promedio": "mean"})
    df_escuela = df_escuela.sort_values(by="nota_promedio", ascending=False)
    df_escuela["nota_promedio"] = df_escuela["nota_promedio"].round(2)

    fig_escuela = go.Figure()
    fig_escuela.add_trace(go.Bar(
        x=df_escuela["nota_promedio"],
        y=df_escuela["escuela_profesional"],
        orientation='h',
        marker=dict(color="#17BECF"),
        text=df_escuela["nota_promedio"],
        textposition="outside"
    ))
    fig_escuela.add_shape(
        type="line",
        x0=promedio_general, x1=promedio_general,
        y0=0, y1=len(df_escuela["escuela_profesional"]),
        line=dict(color="red", dash="dash")
    )
    fig_escuela.add_annotation(
        x=promedio_general,
        y=-1,
        text=f"Promedio: {promedio_general:.2f}",
        showarrow=False,
        font=dict(color="red", size=12)
    )
    fig_escuela.update_layout(
        title="Promedio de Notas por Escuela Profesional",
        xaxis_title="Promedio de Notas",
        yaxis_title="Escuela Profesional",
        yaxis=dict(autorange="reversed")
    )

    # Gráfico por Lugar de Procedencia
    df_procedencia = datos_filtrados.groupby("departamento", as_index=False).agg({"nota_promedio": "mean"})
    df_procedencia = df_procedencia.sort_values(by="nota_promedio", ascending=False)
    df_procedencia["nota_promedio"] = df_procedencia["nota_promedio"].round(2)

    fig_procedencia = go.Figure()
    fig_procedencia.add_trace(go.Bar(
        x=df_procedencia["nota_promedio"],
        y=df_procedencia["departamento"],
        orientation='h',
        marker=dict(color="#2CA02C"),
        text=df_procedencia["nota_promedio"],
        textposition="outside"
    ))
    fig_procedencia.add_shape(
        type="line",
        x0=promedio_general, x1=promedio_general,
        y0=0, y1=len(df_procedencia["departamento"]),
        line=dict(color="red", dash="dash")
    )
    fig_procedencia.add_annotation(
        x=promedio_general,
        y=-1,
        text=f"Promedio: {promedio_general:.2f}",
        showarrow=False,
        font=dict(color="red", size=12)
    )
    fig_procedencia.update_layout(
        title="Promedio de Notas por Lugar de Procedencia",
        xaxis_title="Promedio de Notas",
        yaxis_title="Lugar de Procedencia",
        yaxis=dict(autorange="reversed")
    )

    # Gráfico por Facultad
    df_facultad = datos_filtrados.groupby("facultad", as_index=False).agg({"nota_promedio": "mean"})
    df_facultad = df_facultad.sort_values(by="nota_promedio", ascending=False)
    df_facultad["nota_promedio"] = df_facultad["nota_promedio"].round(2)

    fig_facultad = go.Figure()
    fig_facultad.add_trace(go.Bar(
        x=df_facultad["nota_promedio"],
        y=df_facultad["facultad"],
        orientation='h',
        marker=dict(color="#FF7F0E"),
        text=df_facultad["nota_promedio"],
        textposition="outside"
    ))
    fig_facultad.add_shape(
        type="line",
        x0=promedio_general, x1=promedio_general,
        y0=0, y1=len(df_facultad["facultad"]),
        line=dict(color="red", dash="dash")
    )
    fig_facultad.add_annotation(
        x=promedio_general,
        y=-1,
        text=f"Promedio: {promedio_general:.2f}",
        showarrow=False,
        font=dict(color="red", size=12)
    )
    fig_facultad.update_layout(
        title="Promedio de Notas por Facultad",
        xaxis_title="Promedio de Notas",
        yaxis_title="Facultad",
        yaxis=dict(autorange="reversed")
    )

    # Tabla Resumen
    df_resumen = datos_filtrados.groupby("escuela_profesional", as_index=False).agg({
        "nota_promedio": ["mean", "std", "min", "max", "count"]
    })
    df_resumen.columns = ["Escuela Profesional", "Promedio", "Desviación Estándar", "Mínimo", "Máximo", "Cantidad de Alumnos"]
    df_resumen["Promedio"] = df_resumen["Promedio"].round(2)
    df_resumen["Desviación Estándar"] = df_resumen["Desviación Estándar"].round(2)

    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df_resumen.columns],
        data=df_resumen.to_dict("records"),
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": "#003366",
            "color": "white",
            "fontWeight": "bold"
        },
        style_cell={
            "backgroundColor": "rgb(50, 50, 50)",
            "color": "white",
            "textAlign": "center"
        },
        sort_action="native",
        page_size=28,
    )

    return fig_escuela, fig_procedencia, fig_facultad, table



# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)

import webbrowser
webbrowser.open("http://127.0.0.1:8050/")

