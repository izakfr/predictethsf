from flask import Flask, render_template
import boto3
app = Flask(__name__)

TEAMS_TABLE_NAME = 'dev_esf_team'


@app.route('/')
def hello():
    return 'hello ethSF'

@app.route('/teams')
def landing():
    db = boto3.resource('dynamodb')
    teams_table = db.Table(TEAMS_TABLE_NAME)
    data = teams_table.scan()['Items']
    context = {}
    context['my_string'] = 'StableSquad'
    context['my_list'] = data
    return render_template('landing.html', **context)

@app.route('/instructions')
def instructions():
    return 'instructions'

