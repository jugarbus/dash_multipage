import plotly.graph_objects as go
from data import df_copy, df_num, df_num_2
import dash
from dash import Dash, dcc, html, Input, Output, callback, State

dash.register_page(__name__)


import pandas as pd
import plotly.express as px



fig = px.imshow(
    df_num.corr(),
    labels=dict(color='Correlación'),
    x=df_num.columns,
    y=df_num.columns,
    color_continuous_scale='solar',
    
)


# Layout de la página
heatmap_hombres = px.imshow(
    df_copy[df_copy['SEXO'] == 'Hombre'][df_num.columns].corr(),
    labels=dict(color='Correlación'),
    x=df_num.columns,
    y=df_num.columns,
    color_continuous_scale='agsunset',
    title='Hombres'
)

# Layout de la página
heatmap_mujeres = px.imshow(
    df_copy[df_copy['SEXO'] == 'Mujer'][df_num.columns].corr(),
    labels=dict(color='Correlación'),
    x=df_num.columns,
    y=df_num.columns,
    color_continuous_scale='agsunset',
    title='Mujeres'
)

heatmap_arritmia = px.imshow(
    df_copy[df_copy['AV'] == 'Arritmia'][df_num.columns].corr(),
    labels=dict(color='Correlación'),
    x=df_num.columns,
    y=df_num.columns,
    color_continuous_scale='aggrnyl',
    title='Pacientes con arritmia'
)

heatmap_no_arritmia = px.imshow(
    df_copy[df_copy['AV'] == 'No arritmia'][df_num.columns].corr(),
    labels=dict(color='Correlación'),
    x=df_num.columns,
    y=df_num.columns,
    color_continuous_scale='aggrnyl',
    title='Pacientes sin arritmia'
)


# Layout de la página
layout = html.Div([
    html.H1("Correlación de marcadores numéricos"),
    dcc.Graph(id='heatmap', figure=fig),

    html.H3("Segmentación por Sexo", style={'margin-top': '30px', 'margin-bottom': '15px', 'margin-left': '5%'}),
    html.Div([
        dcc.Graph(id='heatmap-hombres', figure=heatmap_hombres, style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='heatmap-mujeres', figure=heatmap_mujeres, style={'width': '48%', 'display': 'inline-block'})
    ],  style={'display': 'flex', 'justify-content': 'space-between', 'margin-left': '5%', 'margin-right': '5%'}),

    html.H3("Segmentación por AV", style={'margin-top': '30px', 'margin-bottom': '15px', 'margin-left': '5%'}),
    html.Div([
        dcc.Graph(id='heatmap-arritmia', figure=heatmap_arritmia, style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='heatmap-no-arritmia', figure=heatmap_no_arritmia, style={'width': '48%', 'display': 'inline-block'})
    ],  style={'display': 'flex', 'justify-content': 'space-between', 'margin-left': '5%', 'margin-right': '5%'})
])


