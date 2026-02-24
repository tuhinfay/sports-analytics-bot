import requests
from config.settings import FOOTBALL_API_KEY, LEAGUES

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": FOOTBALL_API_KEY
}

def get_todays_matches():
    """Aajker sob matches fetch korbe"""
    from datetime import date
    today = str(date.today())
    
    all_matches = []
    
    for league in LEAGUES:
        url = f"{BASE_URL}/fixtures"
        params = {
            "league": league["id"],
            "season": 2024,
            "date": today
        }
        
        response = requests.get(url, headers=HEADERS, params=params)
        data = response.json()
        
        if data.get("results", 0) > 0:
            for fixture in data["response"]:
                match = {
                    "league": league["name"],
                    "home_team": fixture["teams"]["home"]["name"],
                    "away_team": fixture["teams"]["away"]["name"],
                    "time": fixture["fixture"]["date"],
                    "home_form": get_team_form(fixture["teams"]["home"]["id"]),
                    "away_form": get_team_form(fixture["teams"]["away"]["id"]),
                    "venue": fixture["fixture"]["venue"]["name"],
                }
                all_matches.append(match)
    
    return all_matches

def get_team_form(team_id):
    """Last 5 match er form nebe"""
    url = f"{BASE_URL}/fixtures"
    params = {
        "team": team_id,
        "last": 5
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    
    form = []
    for fixture in data.get("response", []):
        teams = fixture["teams"]
        if teams["home"]["id"] == team_id:
            result = teams["home"]["winner"]
        else:
            result = teams["away"]["winner"]
            
        if result is True:
            form.append("W")
        elif result is False:
            form.append("L")
        else:
            form.append("D")
    
    return "".join(form)

def get_standings(league_id):
    """League standings/table"""
    url = f"{BASE_URL}/standings"
    params = {
        "league": league_id,
        "season": 2024
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    
    standings = []
    if data.get("results", 0) > 0:
        table = data["response"][0]["league"]["standings"][0]
        for team in table[:5]:  # Top 5
            standings.append({
                "rank": team["rank"],
                "team": team["team"]["name"],
                "points": team["points"],
                "played": team["all"]["played"],
                "won": team["all"]["win"],
                "drawn": team["all"]["draw"],
                "lost": team["all"]["lose"],
            })
    
    return standings
