import plotly.graph_objects as go
from data import df_copy, df_num, df_num_2, apply_dimensionality_reduction
import dash
from dash import Dash, dcc, html, Input, Output, callback, State

dash.register_page(__name__)


import pandas as pd
import plotly.express as px

custom_palette={'No arritmia': '#2ca02c', 'Arritmia': '#d62728'}
custom_colors = {"Mujer": "#FF69B4", "Hombre": "#1E90FF"}  



# Preparar datos para el countplot (Distribución de Arritmia)
df_count = df_copy['AV'].value_counts().reset_index()
df_count.columns = ['AV', 'count']

# Dropdown con los valores únicos de las columnas de df_copy
dropdown_values = dcc.Dropdown(
    id='dropdown-values-AV',
    options=[{'label': col, 'value': col} for col in df_num_2.columns],
    value=df_num_2.columns[0],
    clearable=False
)

# Gráfico de Boxplot
boxplot = dcc.Graph(id='boxplot_AV')
histogram = dcc.Graph(id='histogram_AV')


# Dropdown para seleccionar el método de reducción de dimensionalidad
dropdown_dim = dcc.Dropdown(
    id='dimensionality-method',
    options=[
        {'label': 't-SNE', 'value': 't-SNE'},
        {'label': 'PCA', 'value': 'PCA'}
    ],
    value='t-SNE',
    clearable=False
)

graph = dcc.Graph(id='scatter-plot2')

# Dropdown con los valores únicos de las columnas de df_copy
# Gráfico de barras (Countplot de Arritmia)
countplot = dcc.Graph(id='countplot_AV', figure=px.histogram(
    df_copy, x="AV", title="Distribución de la variable AV", 
    text_auto=False, histnorm=None, color="AV"
))



checkbox_sexo = dcc.Checklist(
    id='checkbox-sexo',
    options=[{'label': ' Segmentar por Sexo', 'value': 'Sexo'}],
    value=[],
    inline=True,
    style={
        'fontSize': '20px', 
        'margin': '10px',
        'transform': 'scale(1.5)',  # Aumenta el tamaño del checkbox
        'display': 'inline-block',  # Asegura que se mantenga alineado correctamente
        'padding': '10px'  # Añade espacio alrededor para mejor apariencia
    }
)



# Slider para controlar el número de bins en el histograma
bins_slider2 = dcc.Slider(
    id='bins-slider2',
    min=5,
    max=30,
    step=1,
    value=25,
    marks={i: str(i) for i in range(5, 105, 10)},
    tooltip={"placement": "bottom", "always_visible": True}
)


layout = html.Div([
    html.Div([
        html.Div([
            html.H3("Selección de método"),
            dropdown_dim,
            graph,
            html.Div(checkbox_sexo, style={'margin-left': '40px', 'margin-top': '0px'}), 
            countplot
  
        ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            html.H3("Selección de marcador"),
            dropdown_values,
            boxplot,
            histogram,
            bins_slider2
        ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'justify-content': 'space-around'})
])




@callback(
    Output('scatter-plot2', 'figure'),
    Input('dimensionality-method', 'value')
)
def update_scatter_plot(method):
    reduced_data = apply_dimensionality_reduction(method)
    df_reduced = pd.DataFrame(reduced_data, columns=['Dim1', 'Dim2'])
    df_reduced["PACIENTES"] = df_copy["PACIENTES"]
    df_reduced["SEXO"] = df_copy["SEXO"]
    df_reduced["AV"] = df_copy["AV"].astype(str)
    df_reduced["EDAD"] = df_copy["EDAD"]
    
    fig = px.scatter(
        df_reduced,
        x='Dim1',
        y='Dim2',
        color='AV',
        color_discrete_map=custom_palette,
        custom_data=['PACIENTES', 'SEXO', 'AV', 'EDAD'],
        title=f"Visualización en 2D usando {method}"
    )
    # Configurar el hovertemplate para mostrar PACIENTES, SEXO y EDAD correctamente
    fig.update_traces(
        hovertemplate="<br>".join([
            "ID: %{customdata[0]}",
            "Sexo: %{customdata[1]}",
            "AV: %{customdata[2]}",
            "Edad: %{customdata[3]}",
            "<extra></extra>"  # Elimina el cuadro extra de hover
        ])
    )

    return fig


@callback(
    [Output('boxplot_AV', 'figure'), Output('histogram_AV', 'figure'), Output('countplot_AV', 'figure')],
    [Input('dropdown-values-AV', 'value'), Input('scatter-plot2', 'hoverData'),Input('checkbox-sexo', 'value'), Input('bins-slider2', 'value')]
)
def update_plots(marcador, hover_data, sexo_selected, nbins_slider):
    box_fig = px.box(
        df_copy, 
        x='AV', 
        y=marcador, 
        color='AV', 
        title=f"Distribución de {marcador} según Arritmia",
        color_discrete_map=custom_palette,
        custom_data=['PACIENTES','SEXO','EDAD', marcador]
    )

    hist_fig = px.histogram(
        df_copy, 
        x=marcador, 
        color='AV', 
        title=f"Distribución de {marcador} por Arritmia",
        color_discrete_map=custom_palette,
        nbins=int(nbins_slider),
        barmode="relative"
    )

        # Configurar el hovertemplate para mostrar más información sobre los outliers
    box_fig.update_traces(
        hovertemplate="ID: %{customdata[0]}<br>Sexo: %{customdata[1]}<br>Edad: %{customdata[2]}<br>Valor: %{customdata[3]}<extra></extra>"
    )

    
    
    
    if hover_data:
        hovered_id = hover_data['points'][0]['pointIndex']
        hovered_value = df_num_2.iloc[hovered_id][marcador]

    
        # Agregar línea discontinua en boxplot
        box_fig.add_shape(
                go.layout.Shape(
                    type='line', x0=0, x1=1, y0=hovered_value, y1=hovered_value,
                    xref='paper', yref='y', line=dict(dash='dash', color='red')
                )
            )
            
        hist_fig.add_shape(
                go.layout.Shape(
                    type='line', x0=hovered_value, x1=hovered_value, y0=0, y1=1,
                    xref='x', yref='paper', line=dict(dash='dash', color='red')
                )
            )

    if 'Sexo' in sexo_selected:
        count_fig = px.histogram(
            df_copy, x="AV", color="SEXO", 
            title="Distribución de la variable AV por Sexo",
            text_auto=False, barmode="group",
            color_discrete_map=custom_colors
        )
    else:
        count_fig = px.histogram(
            df_copy, x="AV", title="Distribución de la variable AV", 
            text_auto=False, histnorm=None, color="AV", color_discrete_map=custom_palette
        )

    return box_fig, hist_fig, count_fig