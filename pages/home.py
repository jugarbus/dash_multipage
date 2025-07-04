import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Registrar la página
dash.register_page(__name__, path="/")

layout = html.Div([
    html.H1("Bienvenido al Dashboard de Pacientes con Arritmia"),
    html.P("Este dashboard multipágina te permite explorar diferentes aspectos de los datos de pacientes con arritmia a través de visualizaciones interactivas."),
    
    html.H3("¿Cómo navegar por el dashboard?"),
    html.P("Utiliza el menú de navegación para acceder a las diferentes secciones del dashboard:"),

    html.Ul([
        html.Li([html.B("Inicio"), ": Presentación del dashboard y su funcionalidad."]),
        html.Li([html.B("Marcadores"), " (Dropdown en el menú): Contiene:"]),
        html.Ul([
            html.Li([html.B("Distribuciones"), ": Análisis de la distribución de los marcadores seleccionables."]),
            html.Li([html.B("Heatmaps"), ": Matrices de correlación de los marcadores segmentados por las variables categóricas."]),
        ]),
        html.Li([html.B("Arritmia"), ": Análisis específico de pacientes con y sin arritmia."]),
    ]),

    html.H3("Características interactivas:"),
    html.Ul([
        html.Li([html.B("Reducción de dimensionalidad"), " con selección entre PCA y t-SNE en un dropdown para visualizar la distribución de los datos en un scatterplot."]),
        html.Li([html.B("Selección interactiva de puntos en scatterplot"), " para resaltar datos en boxplots e histogramas."]),
        html.Li([html.B("Selección de marcadores"), " para análisis con dropdown."]),
        html.Li([html.B("Hover sobre los gráficos"), " para mostrar información adicional (scatterplots y outliers de los boxplots)."]),
        html.Li([html.B("Control del número de bins en histogramas"), " con slider ajustable."]),
        html.Li([html.B("Gráfico de barras de distribución de arritmia"), " con segmentación por sexo mediante checkbox."]),
    ]),

], style={
    'margin': 'auto',  # Centra el contenido dentro del div
    'width': '60%',  # Ajusta el ancho para evitar que el texto sea muy ancho
    'padding': '20px'  # Añade algo de espacio alrededor
})

