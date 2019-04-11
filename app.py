import dash
from src import util

app = dash.Dash(__name__)
server = app.server
app.scripts.append_script({"external_url": "https://cdn.plot.ly/plotly-locale-nl-latest.js"})

app.title = "De Politieke Barometer"
app.config.suppress_callback_exceptions = True

party_data = util.load_party_data()
politician_data = util.load_politician_data()