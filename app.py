import dash
from src import util

app = dash.Dash(__name__)
server = app.server

app.title = "De Politieke Barometer"
app.config.suppress_callback_exceptions = True

overview_parties = util.load_overview_parties()
overview_politicians = util.load_overview_politicians()