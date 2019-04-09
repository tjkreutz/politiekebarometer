import dash
from src import util

app = dash.Dash(__name__)
server = app.server
app.scripts.append_script({"external_url": "https://cdn.plot.ly/plotly-locale-nl-latest.js"})

app.title = "De Politieke Barometer"
app.config.suppress_callback_exceptions = True

overview_parties = util.load_overview_parties()
overview_politicians = util.load_overview_politicians()