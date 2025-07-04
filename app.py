import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.io as pio

# Configurar el tema de Plotly para que coincida con SLATE
pio.templates["custom_dark"] = pio.templates["plotly_dark"]
pio.templates["custom_dark"]["layout"]["paper_bgcolor"] = "#272b30"  # Fondo del gráfico
pio.templates["custom_dark"]["layout"]["plot_bgcolor"] = "#272b30"   # Fondo del área de dibujo

# Establecer el tema como predeterminado
pio.templates.default = "custom_dark"

# Crear aplicación Dash para visualización interactiva
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)



ordered_pages = {
    "home": "Inicio",
    "distribuciones": "Distribuciones",
    "heatmap": "Heatmaps",
    "arritmia": "Arritmia"
}

navbar = dbc.Navbar(
    dbc.Container([
        # Botón de Inicio
        dbc.NavbarBrand("Dashboard Arritmia.csv", className="ms-2"),

        dbc.Nav([
            # Enlace a la página de Inicio
            dbc.NavItem(dbc.NavLink("Inicio", href="/", active="exact")),

            # Dropdown para Marcadores con Distribuciones y Heatmap
            dbc.DropdownMenu(
                label="Marcadores",
                children=[
                    dbc.DropdownMenuItem("Distribuciones", href="/distribuciones"),
                    dbc.DropdownMenuItem("Heatmaps", href="/heatmap"),
                ],
                nav=True,
                in_navbar=True,
            ),

            # Enlace a la página de Arritmia
            dbc.NavItem(dbc.NavLink("Arritmia", href="/arritmia", active="exact")),
        ], className="ms-auto")
    ]),
    color="primary",
    dark=True,
    className="mb-2"
)


app.layout = dbc.Container([
    navbar,
    dash.page_container  # Contenedor para el manejo de páginas dinámicas en Dash
], fluid=True)



# Ejecutar la aplicación en modo debug para desarrollo
if __name__ == "__main__":
    app.run_server(debug=True)