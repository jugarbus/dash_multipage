import plotly.graph_objects as go
from data import df_copy, df_num, df_num_2, apply_dimensionality_reduction
import dash
from dash import Dash, dcc, html, Input, Output, callback, State

dash.register_page(__name__)


import pandas as pd
import plotly.express as px


custom_palette={'No arritmia': '#2ca02c', 'Arritmia': '#d62728'}




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

graph = dcc.Graph(id='scatter-plot')

# Dropdown con los valores únicos de las columnas de df_copy
dropdown_values = dcc.Dropdown(
    id='dropdown-values',
    options=[{'label': col, 'value': col} for col in df_num_2.columns],
    value=df_num_2.columns[0],
    clearable=False
)


boxplot = dcc.Graph(id='boxplot')



histogram = dcc.Graph(id='histogram')



# Slider para controlar el número de bins en el histograma
bins_slider = dcc.Slider(
    id='bins-slider',
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
            html.H4("Selección de método de reducción de dimensionalidad"),
            dropdown_dim,
            graph,
               
        ], style={
    'width': '40%',
    'display': 'block',  # Cambia de 'inline-block' a 'block' para aplicar auto margin
    'marginLeft': 'auto',
    'marginRight': 'auto',
    'marginTop': '12%',
    'textAlign': 'center'  # Alinea el texto e hijos al centro
}),
        
        html.Div([
            html.H3("Selección de marcador"),
            dropdown_values,
            boxplot,
            histogram, 
            bins_slider
        ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-right': '5%'})
])




# Callback para actualizar el gráfico según el método de reducción de dimensionalidad seleccionado
@callback(
    Output('scatter-plot', 'figure'),
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


# Callback para actualizar los gráficos según la variable seleccionada
@callback(
    [Output('boxplot', 'figure'), Output('histogram', 'figure')],
    [Input('dropdown-values', 'value'), Input('scatter-plot', 'hoverData'), Input('bins-slider', 'value')]
)
def update_graphs(variable, hover_data, nbins_slider):


    df_num_2["PACIENTES"] = df_copy["PACIENTES"]
    df_num_2["SEXO"] = df_copy["SEXO"]
    df_num_2["AV"] = df_copy["AV"].astype(str)
    df_num_2["EDAD"] = df_copy["EDAD"]

    box_fig = px.box(df_num_2, y=variable, 
                 title=f"Boxplot de {variable}", 
                 custom_data=['PACIENTES','SEXO','EDAD', variable])

    hist_fig = px.histogram(df_num_2, x=variable, 
                        nbins=nbins_slider, 
                        title=f"Histograma de {variable}")


    
    box_fig.update_traces(
    hovertemplate="ID: %{customdata[0]}<br>Sexo: %{customdata[1]}<br>Edad: %{customdata[2]}<br>Valor: %{customdata[3]}<extra></extra>"
    )
    
    if hover_data:
        hovered_id = hover_data['points'][0]['pointIndex']
        hovered_value = df_num_2.iloc[hovered_id][variable]

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
    
    
    return box_fig, hist_fig 