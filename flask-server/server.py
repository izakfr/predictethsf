from flask import Flask, render_template
from teams.TeamModel import TeamModel
from utils import DEV_PROD_VALUE

app = Flask(__name__)


@app.route('/test')
def hello():
    return 'Hello EthSF'

@app.route('/')
def index():
    results = TeamModel.scan()
    dict_results = sorted([dict(x) for x in results], key=lambda x: float(x['total_staked_ether']), reverse=True)
    context = {}
    context['my_string'] = 'My first string'
    context['teams_list'] = dict_results
    return render_template('landing.html', **context)


@app.route('/stage')
def stage():
    return 'Stage: ' + DEV_PROD_VALUE('dev', 'prod')