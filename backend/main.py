import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import os


#create app object
app = FastAPI()

#structure is used for JSON validation, with python type declaration FastAPI will perform below operations on the request data
# 1) reads body of request as JSON
# 2) convert corresponding types
# 3) validate the data, if the data is invalid it will return an error indiciating where and what was the incorrect data

class LeagueChurn(BaseModel):
    league_points: int
    rank: str
    wins: int
    losses: int
    veteran: bool
    fresh_blood: bool
    hot_streak: bool
    tier: str
    game_version: str
    assists: int
    kills: int
    deaths: float
    lane: str
    champion_name: str
    gold_earned: int
    turret_kills: int
    total_dmg_dealt: int
    total_heal: int
    vision_score: int
    summoner_level: int
    time_played: int
    KDA: float
    WL: float
    gold_earned_per_min: float


@app.get('/')
def index():
    return {'message': 'Hello'}

@app.get('/home')
def get_home():
    return {'message': 'You are Home'}

@app.post('/predict')
def predict_summoner(data:LeagueChurn):

    CURRENT_DIR = os.path.dirname(__file__)
    with open(os.path.abspath(os.path.join(CURRENT_DIR, 'model_pkl')), 'rb') as file:
        model = pickle.load(file)

    data = data.dict()
    league_points = data['league_points']
    rank = data['rank']
    wins = data['wins']
    losses = data['losses']
    veteran = data['veteran']
    fresh_blood = data['fresh_blood']
    hot_streak = data['hot_streak']
    tier = data['tier']
    game_version = data['game_version']
    assists = data['assists']
    kills = data['kills']
    deaths = data['deaths']
    lane = data['lane']
    champion_name = data['champion_name']
    gold_earned = data['gold_earned']
    turret_kills = data['turret_kills']
    total_dmg_dealt = data['total_dmg_dealt']
    total_heal = data['total_heal']
    vision_score = data['vision_score']
    summoner_level = data['summoner_level']
    time_played = data['time_played']
    KDA = data['KDA']
    WL = data['WL']
    gold_earned_per_min = data['gold_earned_per_min']

    X = pd.DataFrame([[league_points, rank, wins, losses, veteran, fresh_blood, hot_streak, tier,
    game_version, assists, kills, deaths, lane, champion_name, gold_earned, turret_kills,
    total_dmg_dealt, total_heal, vision_score, summoner_level, time_played, KDA,
    WL, gold_earned_per_min]], columns=data.keys())
    
    prediction = model.predict(X)

    if(prediction[0]):
        pred = "Churned"
    else:
        pred = "Did not churn"

    return {'prediction': pred
    }


if __name__== '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
#uvicorn main:app --reload