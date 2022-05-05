from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap

from cricket_data import get_upcoming_matches, live_score

FONT = ('Ubuntu', 20, 'bold')



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hfas8qewjkjqk4hgmv9878$#'

bootstrap = Bootstrap(app)

UPCOMING_MATCHES = get_upcoming_matches()
UPCOMING_MATCHES = UPCOMING_MATCHES[: 3]

match_id = None
for match in UPCOMING_MATCHES[: 1]:
    match_id = match['id']

SCORE_LIVE = live_score(match_id)

live_details = {
    "batting_team": "",
    "bats_man": "",
    "runs": "",
    "bowling_team": "",
    "bowler": "",
    "wickets": "",
    "overs": "",
}


@app.route('/')
def home():
    if SCORE_LIVE['live_details'] == None:
        date = SCORE_LIVE['fixture']['start_date'].split('T')[0]
        flash (f'No match right Now! Next Match is on {date}')
    else:
        ongoing = SCORE_LIVE['live_details']
        if ongoing['scorecard'][0]['current'] == True:
            live_details['batting_team'] = ongoing['scorecard'][0]['title']
            live_details['bats_man'] = ongoing['scorecard'][0]['batting'][-1]['player_name']
            live_details['runs'] = ongoing['scorecard'][0]['runs']
            live_details['wickets'] = ongoing['scorecard'][0]['wickets']
            live_details['overs'] = ongoing['scorecard'][0]['overs']
            live_details['bowling_team'] = ongoing['scorecard'][1]['title']
            live_details['bowler'] = ongoing['scorecard'][1]['bowling'][-1]['player_name']

        elif ongoing['scorecard'][1]['current'] == True:
            live_details['batting_team'] = ongoing['scorecard'][1]['title']
            live_details['bats_man'] = ongoing['scorecard'][1]['batting'][-1]['player_name']
            live_details['runs'] = ongoing['scorecard'][1]['runs']
            live_details['wickets'] = ongoing['scorecard'][1]['wickets']
            live_details['overs'] = ongoing['scorecard'][1]['overs']
            live_details['bowling_team'] = ongoing['scorecard'][0]['title']
            live_details['bowler'] = ongoing['scorecard'][0]['bowling'][-1]['player_name']
    
    return render_template('home.html', ongoing=live_details)

@app.route('/upcoming-events')
def upcoming_events():
    return render_template('up_matches.html', upcoming_matches=UPCOMING_MATCHES)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
