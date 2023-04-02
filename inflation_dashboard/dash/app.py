import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

from inflation_dashboard.dash.src.all_categories_tab import all_content
from inflation_dashboard.dash.src.core_and_headline_tab import headline_and_core_content
from inflation_dashboard.dash.src.edu_tab import edu_content
from inflation_dashboard.dash.src.energy_tab import energy_content
from inflation_dashboard.dash.src.food_tab import food_content
from inflation_dashboard.dash.src.housing_tab import housing_content
from inflation_dashboard.dash.src.medical_tab import medical_content
from inflation_dashboard.dash.src.overview_tab import overview_content

app = Dash(__name__, external_stylesheets=[dbc.themes.YETI])
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "24rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H4("CPI Report", className="display-4"),
        html.Hr(),
        html.P("CPI Category", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Core & Headline", href="/coreandheadline", active="exact"),
                dbc.NavLink("Energy", href="/energy", active="exact"),
                dbc.NavLink("Food", href="/food", active="exact"),
                dbc.NavLink("Education", href="/education", active="exact"),
                dbc.NavLink("Housing", href="/housing", active="exact"),
                dbc.NavLink("Medical", href="/medical", active="exact"),
                dbc.NavLink("All Categories", href="/all", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return overview_content
    elif pathname == "/coreandheadline":
        return headline_and_core_content
    elif pathname == "/food":
        return food_content
    elif pathname == "/energy":
        return energy_content
    elif pathname == "/education":
        return edu_content
    elif pathname == "/housing":
        return housing_content
    elif pathname == "/medical":
        return medical_content
    elif pathname == "/all":
        return all_content
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
