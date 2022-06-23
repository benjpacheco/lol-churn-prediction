import streamlit
import requests

#simple ui built using streamlit
#text_input for any number inputs required
#selectbox for any categorical inputs required

def run():
    streamlit.title("League of Legends Churn Predictor")
    league_points = streamlit.text_input("League Points")
    rank = streamlit.selectbox("Rank", ["I", "II", "III", "IV"])
    wins = streamlit.text_input("Wins")
    losses = streamlit.text_input("Losses")
    veteran = streamlit.selectbox("Veteran", ["True", "False"])
    fresh_blood = streamlit.selectbox("Fresh Blood", ["True", "False"])
    hot_streak = streamlit.selectbox("Hot Streak", ["True", "False"])
    tier = streamlit.selectbox("Tier", [
                               "IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND", "MASTER", "CHALLENGER"])
    game_version = streamlit.selectbox("Patch", ["12.1.416.4011", "12.5.425.9171", "12.7.433.4138", "12.8.437.6765", "12.2.419.1399", "11.24.414.4003", "11.23.409.111", "12.6.432.1258", "12.3.421.5967", "12.4.423.2790", "12.9.439.127", "11.22.406.3587",
                                        "11.20.400.7328", "11.21.403.3002", "11.15.389.2308", "11.17.394.4489", "11.19.398.9466", "11.24.413.2485", "11.18.395.7538", "11.1.352.5559", "11.16.390.1945", "11.14.385.9967", "11.7.366.7612", "11.6.365.1420",
                                        "12.8.436.3750", "11.2.353.8505", "11.9.372.2066", "11.13.382.1241", "11.11.377.6311", "11.8.370.4668", "11.12.379.4946", "11.5.361.3108", "11.3.357.5376", "11.4.360.513", "10.25.350.1724", "11.10.376.4811",
                                        "12.6.430.6775", "11.10.374.9538", "11.15.388.2387", "12.3.420.4308", "11.24.412.2185", "12.3.421.3734", "12.6.431.7988", "10.25.348.1797", "11.17.393.607", "11.6.364.2723", "11.3.356.7268", "12.1.414.6260", 
                                        "11.19.398.2521", "11.1.351.8352", "12.2.418.8114", "11.14.384.6677", "11.15.387.5736", "11.8.369.4139", "11.4.358.8046"])
    assists = streamlit.text_input("Assists")
    kills = streamlit.text_input("Kills")
    deaths = streamlit.text_input("Deaths")
    lane = streamlit.selectbox(
        "Lane", ["BOTTOM", "JUNGLE", "MIDDLE", "TOP", "NONE"])
    champion_name = streamlit.selectbox("Champion", ["Lux", "Morgana", "MissFortune", "Jhin", "Kaisa", "Jinx", "Yasuo", "Teemo", "MasterYi", "Sett", "Warwick", "Ashe", "Caitlyn", "Akali", "Kayn", "Yone", "Tristana", "Mordekaiser", "Brand", "Ahri",
                                        "Seraphine", "Pyke", "Garen", "Nautilus", "Vayne", "Senna", "Yuumi", "Kayle", "Jax", "Swain", "Blitzcrank", "Diana", "Malzahar", "Soraka", "Volibear", "Nasus", "Veigar", "Ezreal", "Ekko", "Nocturne", "Urgot",
                                        "Nami", "Zed", "Sivir", "Galio", "Tryndamere", "Ziggs", "Vex", "Darius", "Lillia", "Nunu", "LeeSin", "Vi", "Leona", "TahmKench", "Viego", "Irelia", "Kindred", "Chogath", "Heimerdinger", "Shaco", "Velkoz", "DrMundo",
                                        "Illaoi", "Xerath", "Graves", "Samira", "Twitch", "Neeko", "Sion", "XinZhao", "Thresh", "Varus", "Pantheon", "Amumu", "Lulu", "Lucian", "Xayah", "Malphite", "Sona", "Rakan", "Zyra", "Aphelios", "Akshan", "Sylas",
                                        "Talon", "Katarina", "Janna", "Hecarim", "JarvanIV", "Fiora", "Sejuani", "Fizz", "Leblanc", "Khazix", "Yorick", "Shyvana", "Trundle", "Gwen", "Poppy", "FiddleSticks", "Evelynn", "Rammus", "Gangplank", "Gnar", "Ornn",
                                        "Aatrox", "Udyr", "Draven", "Shen", "Zeri", "Olaf", "MonkeyKing", "TwistedFate", "Karma", "Zoe", "Karthus", "Renekton", "Quinn", "Viktor", "Annie", "Riven", "Camille", "Zac", "Renata", "Singed", "Corki", "Zilean",
                                        "Qiyana", "Ryze", "Anivia", "Jayce", "Taliyah", "Nidalee", "Kennen", "Taric", "Bard", "Cassiopeia", "Vladimir", "Alistar", "Orianna", "Rengar", "Braum", "Syndra", "Maokai", "Elise", "KogMaw", "Kassadin", "RekSai",
                                        "Kalista", "AurelionSol", "Kled", "Gragas", "Rell", "Ivern", "Azir", "Lissandra", "Rumble", "Skarner"])
    gold_earned = streamlit.text_input("Gold Earned")
    turret_kills = streamlit.text_input("Turret Kills")
    total_dmg_dealt = streamlit.text_input("Total Damage Dealt")
    total_heal = streamlit.text_input("Total Heals")
    vision_score = streamlit.text_input("Vision Score")
    summoner_level = streamlit.text_input("Summoner Level")
    time_played = streamlit.text_input("Time Played (sec)")
    KDA = streamlit.text_input("Kill Death Assists Ratio")
    WL = streamlit.text_input("Win Loss Ratio")
    gold_earned_per_min = streamlit.text_input("Gold Earned Per Min")

    data = {
        "league_points": league_points,
        "rank": rank,
        "wins": wins,
        "losses": losses,
        "veteran": veteran,
        "fresh_blood": fresh_blood,
        "hot_streak": hot_streak,
        "tier": tier,
        "game_version": game_version,
        "assists": assists,
        "kills": kills,
        "deaths": deaths,
        "lane": lane,
        "champion_name": champion_name,
        "gold_earned": gold_earned,
        "turret_kills": turret_kills,
        "total_dmg_dealt": total_dmg_dealt,
        "total_heal": total_heal,
        "vision_score": vision_score,
        "summoner_level": summoner_level,
        "time_played": time_played,
        "KDA": KDA,
        "WL": WL,
        "gold_earned_per_min": gold_earned_per_min
    }
    #posts to same port the backends runs on 
    if streamlit.button("Predict"):
        response = requests.post("http://backend:8000/predict", json=data)
        prediction = response.text
        streamlit.success(f"The predicion from model: {prediction}")

if __name__ == '__main__':
    #runs at 8501 port
    run()
