#importing packages
import os
import json
import requests
import pandas as pd
import numpy as np
import time
import schedule
import math
from datetime import datetime
import logging
from dotenv import find_dotenv, load_dotenv


class Data:
  def __init__(self):
        self.league_list = []
        self.summoner_list = []
        self.match_list = []
        self.puuid_list = []
        self.list_of_tiers = ["IRON/I", "IRON/II", "IRON/III", "IRON/IV", "BRONZE/I",  "BRONZE/II", "BRONZE/III", "BRONZE/IV", "SILVER/I",
        "SILVER/II", "SILVER/III", "SILVER/IV", "GOLD/I", "GOLD/II", "GOLD/III", "GOLD/IV", "PLATINUM/I", "PLATINUM/II", "PLATINUM/III",
        "PLATINUM/IV", "DIAMOND/I", "DIAMOND/II",  "DIAMOND/III", "DIAMOND/IV"]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com"
            }
        self.lower_league_url = "https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/"
        self.upper_league_urls = ["https://na1.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key="+api_key,
                "https://na1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key="+api_key,
                "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key="+api_key,]

        self.summoner_url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
        self.puuid_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"
        self.match_url = "https://americas.api.riotgames.com/lol/match/v5/matches/"


class Timedout:
    def __init__(self, list_of_names, result_list, url, case):
        self.list_of_names = list_of_names
        self.result_list = result_list
        self.url = url
        self.case = case
        self.number_of_requests_per_limit = 100
        self.number_of_iterations = math.ceil(len(self.list_of_names)/ self.number_of_requests_per_limit)
        self.batch = 0
        self.interval_in_seconds = 120 #120 seconds is our limit here
        self.execution_time = 0
        

    def lower_league_requests(self):
        for i in range (0, self.number_of_requests_per_limit):
            # we don't want to access the index for the element out of list
            try:
                for tier in self.list_of_names:
                    for page in range(1, 11, 1):
                        url = self.url+tier+"?page="+str(page)+"&api_key="+api_key
                        req = requests.get(url, headers=data_obj.headers)
                        print(req.status_code)
                        if req.status_code == 200:
                            data_json = json.loads(req.text)
                            self.result_list.extend(data_json)
            except (IndexError, KeyError) as error:
                break 

    def upper_league_requests(self):
        for i in range (0, self.number_of_requests_per_limit):
            # we don't want to access the index for the element out of list
            try:
                for url in self.list_of_names:
                    req = requests.get(url, headers=data_obj.headers)
                    if req.status_code == 200:
                        data_json = json.loads(req.text)
                        for entry in data_json['entries']:
                            entry['tier'] = data_json['tier']
                            entry['leagueId'] = data_json['leagueId']
                            entry['queue'] = data_json['queue']
                            data_obj.league_list.append(entry)
            except (IndexError, KeyError) as error:
                break  

    def match_summoner_requests(self):
        for i in range (0, self.number_of_requests_per_limit):
            # we don't want to access the index for the element out of list
            try:
                url = url+self.list_of_names[i]+"?api_key="+api_key
                req = requests.get(url, headers=data_obj.headers)
                if req.status_code == 200:
                    data_json = json.loads(req.text)
                    self.result_list.append(data_json)
            except (IndexError, KeyError) as error:
                break

    def request_name(self):
        start_time = time.time()
        
        if (self.case == "lower_league"):
            self.lower_league_requests()
        if (self.case == "upper_league"):
            self.upper_league_requests()
        if (self.case == "match_summoner"):
            self.match_summoner_requests()
        
    
        if(len(self.list_of_names) > self.number_of_requests_per_limit):
            # slice list_of_names so the next time request_name is called it will call the next batch
            self.list_of_names = self.list_of_names[self.number_of_requests_per_limit:].reset_index(drop=True)
        self.execution_time = time.time() - start_time

    def my_schedule(self):
        while 1:
            if (self.batch >= self.number_of_iterations):
                break
            print("Batch number", self.batch)
            Timedout.request_name(self)
            schedule.run_pending()
            sleep_time = self.interval_in_seconds - self.execution_time
            if (sleep_time < 0):
                sleep_time = 0
            print("Sleep for: ", sleep_time)
            time.sleep(sleep_time)
            self.batch += 1


class LeagueDataFrame:

    def __init__(self, league_list):
        self.league_list = league_list
        self.CURRENT_DIR = os.path.dirname(__file__)
        self.league_dict_list = []
        self.summoner_names 
        self.league_data

    def replace_url_spaces(self, somelist):
        for data in somelist:
            data = data.replace(' ', '%20')
        return somelist

    def create_league_df(self):

        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/league_json.json')), mode='a') as file:
    
            for league in self.league_list:
                league.pop("miniSeries", None)
                league.pop("entries", None)
                league.pop("name", None)
                try:
                    json.dump(league, file)
                    file.write('\n')
                except Exception as e:
                    print("No league found: {} with error {}".format(str(league), str(e)))

        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/league_json.json')), encoding='utf-8') as json_file:
            for line in json_file:
                json_data = json.loads(line)
                self.league_dict_list.append(json_data)
        if json_data:
            self.league_data = pd.DataFrame(self.league_dict_list, columns = json_data.keys())
        self.league_data = self.league_data.rename(columns={'summonerName': 'summoner_name', 'leaguePoints': 'league_points',
                                            'freshBlood': 'fresh_blood', 'hotStreak': 'hot_streak',})

        self.summoner_names = self.replace_url_spaces(league_data['summonerName'])
 
class SummonerDataFrame:

    def __init__(self, summoner_list):
        self.summoner_list = summoner_list
        self.CURRENT_DIR = os.path.dirname(__file__)
        self.summoner_dict_list = []
        self.match_puuids = []

    def create_summoner_df(self):

        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/summoner_json.json')), mode='a') as file:
            for summoner in self.summoner_list:
                try:
                    json.dump(summoner, file)
                    file.write('\n')
                except Exception as e:
                    print("No summoner found: {} with error {}".format(str(summoner), str(e)))

        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/summoner_json.json')), encoding='utf-8') as json_file:
            for line in json_file:
                json_data = json.loads(line)
                self.summoner_dict_list.append(json_data)
        if json_data:
            summoner_data = pd.DataFrame(self.summoner_dict_list, columns = json_data.keys())

        self.match_puuids = summoner_data['puuid']


class PuuidJson:

    def __init__(self, puuid_list):
        self.puuid_list = puuid_list
        self.CURRENT_DIR = os.path.dirname(__file__)
        self.puuid_flattened_list = []

    def create_puuid_json(self):
        
        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/puuid_json.json')), mode='a') as file:
            flat_list = list(np.concatenate(self.puuid_list).flat)
            for puuid in flat_list:
                try:
                    json.dump(puuid, file)
                    file.write('\n')
                except Exception as e:
                    print("No puuid found: {} with error {}".format(str(puuid), str(e)))

        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/puuid_json.json')), encoding='utf-8') as json_file:
            for line in json_file:
                json_data = json.loads(line)
                self.puuid_flattened_list.append(json_data)

        return self.puuid_flattened_list

class MatchDataFrame:

    def __init__(self, match_list):
        self.match_list = match_list
        self.CURRENT_DIR = os.path.dirname(__file__)
        self.match_dict_list = []
        self.match_data

    def create_match_df(self):
        
        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/match_json.json')), mode='a') as file:
            for match in self.match_list:
                try:
                    json.dump(match, file)
                    file.write('\n')
                except Exception as e:
                    print("No match found: {} with error {}".format(str(match), str(e)))

        with open(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", '../data/raw/match_json.json')), encoding='utf-8') as json_file:
            for line in json_file:
                json_data = json.loads(line)
                try:
                    for participant in json_data['info']['participants']:
                        participant_dict = {}
                        participant_dict['match_id'] = json_data['metadata']['matchId']
                        # if the key exists in dictionary then add the end time stamp
                        if 'gameEndTimestamp' in json_data['info']:
                            participant_dict['game_end_timestamp'] = json_data['info']['gameEndTimestamp']
                        # else set the value to null and handle it later in DF
                        else:
                            participant_dict['game_end_timestamp'] = np.nan
                        participant_dict['game_start_timestamp'] = json_data['info']['gameStartTimestamp']
                        participant_dict['game_id'] = json_data['info']['gameId']
                        participant_dict['game_version'] = json_data['info']['gameVersion']
                        participant_dict['assists'] = participant['assists']
                        participant_dict['kills'] = participant['kills']
                        participant_dict['deaths'] = participant['deaths']
                        participant_dict['lane'] = participant['lane']
                        participant_dict['champion_name'] = participant['championName']
                        participant_dict['gold_earned'] = participant['goldEarned']
                        participant_dict['gold_spent'] = participant['goldSpent']
                        participant_dict['turret_kills'] = participant['turretKills']
                        participant_dict['total_dmg_dealt'] = participant['totalDamageDealt']
                        participant_dict['total_heal'] = participant['totalHeal']
                        participant_dict['vision_score'] = participant['visionScore']
                        participant_dict['puuid'] = participant['puuid']
                        participant_dict['summoner_level'] = participant['summonerLevel']
                        participant_dict['summoner_name'] = participant['summonerName']
                        participant_dict['time_played'] = participant['timePlayed']
                        #append to list
                        self.match_dict_list.append(participant_dict)
                except KeyError as error:
                        print(json_data['info'])
                        break
        self.match_data = pd.DataFrame(self.match_dict_list, columns = participant_dict.keys())
        self.match_data = self.match_data.drop_duplicates()
        missing_end_timestamps = self.match_data['game_start_timestamp'] + self.match_data['time_played']
        self.match_data['game_end_timestamp'] = self.match_data['game_end_timestamp'].fillna(missing_end_timestamps)



class MasterDataFrame:

    def __init__(self, league_data, match_data):
        self.league_data = league_data
        self.match_data = match_data
        self.CURRENT_DIR = os.path.dirname(__file__)

    def create_master_df(self):
        
        master_df = pd.merge(left=self.league_data, right=self.match_data, how='inner', on='summoner_name')
        master_df = master_df.drop(['summonerId', 'leagueId', 'game_id', 'puuid'], axis=1)

        master_df.game_end_timestamp = master_df.game_end_timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000).strftime("%Y-%m-%d %H:%M:%S"))
        master_df.game_start_timestamp = master_df.game_start_timestamp.apply(lambda x: datetime.utcfromtimestamp(x/1000).strftime("%Y-%m-%d %H:%M:%S"))
        master_df.game_end_timestamp = pd.to_datetime(master_df.game_end_timestamp, errors='coerce', format='%Y-%m-%d %H:%M:%S')
        master_df.game_start_timestamp = pd.to_datetime(master_df.game_start_timestamp, errors='coerce', format='%Y-%m-%d %H:%M:%S')

        last_game_played = master_df.sort_values(by=['game_end_timestamp']).drop_duplicates(subset='summoner_name', keep='last')
        master_df['last_match'] = last_game_played['game_end_timestamp']
        master_df['last_match'] = master_df.groupby('summoner_name')['last_match'].ffill().bfill()
        master_df = master_df.drop('gold_spent', axis=1)
        master_df.to_csv(os.path.abspath(os.path.join(self.CURRENT_DIR, "..", "../data/processed/master_lol_churn_prediction.csv")), index=False)
        

def main():
    """ Runs data processing scripts to extract from API endpoints then save raw data and turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    api_key = str(os.getenv("API_KEY"))


    #instatiate data class
    data_obj = Data()

    #get the league data
    lower_league_list_timeout = Timedout(data_obj.list_of_tiers, data_obj.league_list, data_obj.lower_league_url, "lower_league")
    lower_league_list_timeout.my_schedule()
    upper_league_list_timeout = Timedout(data_obj.upper_league_urls, data_obj.league_list, "", "upper_league")
    upper_league_list_timeout.my_schedule()
    league_data = LeagueDataFrame(data_obj.league_list)
    league_data.create_league_df()

    #get the summoner data
    summoner_list_timeout = Timedout(league_data.summoner_names, data_obj.summoner_list, data_obj.summoner_url, "match_summoner")
    summoner_list_timeout.my_schedule()
    summoner_data = SummonerDataFrame(data_obj.summoner_list)
    summoner_data.create_summoner_df()

    #get the puuid data
    puuid_list_timeout = Timedout(summoner_data.match_puuids, data_obj.puuid_list, data_obj.puuid_url, "match_summoner")
    puuid_list_timeout.my_schedule()
    puuid_data = PuuidJson(data_obj.puuid_list)
    puuid_data.create_puuid_json()

    #get the match data
    match_list_timeout = Timedout(puuid_data.puuid_flattened_list, data_obj.match_list, data_obj.match_url, "match_summoner")
    match_list_timeout.my_schedule()
    match_data = MatchDataFrame(data_obj.match_list)
    match_data.create_match_df()

    #join league and match data and create master df
    master_df = MasterDataFrame(league_data.league_data, match_data.match_data)
    master_df.create_master_df()


    main()