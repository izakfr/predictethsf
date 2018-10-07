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

    global_staked_ether = 0.0

    for team in dict_results:
    	global_staked_ether += float(team['total_staked_ether'])

    for team in dict_results:
    	team['implied_win'] = round((float(team['total_staked_ether']) / global_staked_ether) * 100, 2)
    	team['total_staked_ether'] = round(float(team['total_staked_ether']), 3)
    	if team['picture_url'] == None:
    		team['picture_url'] = 'https://i.imgur.com/v3TqVnb.jpg'
    	if team['project_link'] == None:
    		team['project_link'] = ''
    	if team['description'] == None:
    		team['description'] = ''

    context = {}

    context['my_string'] = 'My first string'
    context['teams_list'] = dict_results
    return render_template('index.html', **context)


@app.route('/stage')
def stage():
    return 'Stage: ' + DEV_PROD_VALUE('dev', 'prod')