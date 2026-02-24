import requests
import os
from datetime import date
from config.settings import FOOTBALL_API_KEY, LEAGUES

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": FOOTBALL_API_KEY}

def download_image(url, path):
    """Image download kore save korbe"""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
            return path
    except:
        pass
    return None

def get_team_form(team_id):
    """Last 5 match er form"""
    url = f"{BASE_URL}/fixtures"
    params = {"team": team_id, "last": 5}
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

def get_team_stats(team_id, league_id, season=2024):
    """Team er detailed stats"""
    url = f"{BASE_URL}/teams/statistics"
    params = {"team": team_id, "league": league_id, "season": season}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    
    if not data.get("response"):
        return {}
    
    stats = data["response"]
    return {
        "goals_for": stats.get("goals", {}).get("for", {}).get("total", {}).get("total", 0),
        "goals_against": stats.get("goals", {}).get("against", {}).get("total", {}).get("total", 0),
        "wins": stats.get("fixtures", {}).get("wins", {}).get("total", 0),
        "draws": stats.get("fixtures", {}).get("draws", {}).get("total", 0),
        "loses": stats.get("fixtures", {}).get("loses", {}).get("total", 0),
    }

def get_todays_matches():
    """Aajker sob matches with full details"""
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
                home = fixture["teams"]["home"]
                away = fixture["teams"]["away"]
                
                # Team logos download
                home_logo_path = f"temp/logos/{home['id']}.png"
                away_logo_path = f"temp/logos/{away['id']}.png"
                download_image(home["logo"], home_logo_path)
                download_image(away["logo"], away_logo_path)
                
                # Stats
                home_stats = get_team_stats(home["id"], league["id"])
                away_stats = get_team_stats(away["id"], league["id"])
                
                match = {
                    "league": league["name"],
                    "league_id": league["id"],
                    "match_date": today,
                    "home_team": home["name"],
                    "home_id": home["id"],
                    "home_logo": home_logo_path,
                    "home_form": get_team_form(home["id"]),
                    "home_stats": home_stats,
                    "away_team": away["name"],
                    "away_id": away["id"],
                    "away_logo": away_logo_path,
                    "away_form": get_team_form(away["id"]),
                    "away_stats": away_stats,
                    "time": fixture["fixture"]["date"],
                    "venue": fixture["fixture"]["venue"]["name"] or "TBD",
                }
                all_matches.append(match)
    
    return all_matches