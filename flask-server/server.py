from flask import Flask, render_template, request, redirect
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
    	if global_staked_ether == 0:
    		team['implied_win'] = 0
    	else:
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

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    title = request.form['title']
    link = request.form['link']
    url = request.form['url']
    description = request.form['description']
    tx_hash = request.form['tx_hash']

    new_team = TeamModel(
        tx_hash,
        name=title,
        description=description,
        picture_url=url,
        project_link=link,
    )
    new_team.save()
    return redirect('/')

@app.route('/stage')
def stage():
    return 'Stage: ' + DEV_PROD_VALUE('dev', 'prod')