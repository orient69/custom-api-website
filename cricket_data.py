import requests


WEB_ENDPOINT = 'https://cricket-live-data.p.rapidapi.com'
API_KEY = '08f75265bdmshad39d15b296337cp1109b4jsn0c76605b29d8'

HEADERS = {
    'X-RapidAPI-Host': 'cricket-live-data.p.rapidapi.com',
    'X-RapidAPI-Key': API_KEY,
    # 'x-rapidapi-region': 'AWS - ap-south-1',

    }

def get_upcoming_matches():
    league_response = requests.get(f'{WEB_ENDPOINT}/series', headers= HEADERS).json()['results'][2]['series']

    ipl = None
    for league in league_response:
        if league['series_name'] == 'Indian Premier League':
            ipl = league
            break

    url = f"https://cricket-live-data.p.rapidapi.com/fixtures-by-series/{ipl['series_id']}"

    matches = requests.get(url, headers=HEADERS).json()['results']

    upcoming_matches = []
    for match in matches[:: -1]:
        if match['status'] != 'Complete':
            date_data = match['date']
            formatted_date = date_data.split('T')[0]
            match['date'] = formatted_date
            upcoming_matches.append(match)
        else:
            break

    upcoming_matches = upcoming_matches[:: -1]
    
    return upcoming_matches


def live_score(match_id):
    url_score = f"https://cricket-live-data.p.rapidapi.com/match/{match_id}"

    response_score = requests.get(url_score, headers=HEADERS).json()['results']
    return response_score
