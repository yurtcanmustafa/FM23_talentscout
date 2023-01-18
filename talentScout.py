import pandas as pd

pd.set_option("display.width", 500)
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: "%.2f" % x)

# Veri Okuma / Player Database
def read_data():
    df = pd.read_excel(r"FM_2023_final.xlsx")
    df.set_index("Name", inplace=True)
    return df

df = read_data()
df.head()

def calculate_corr(dataframe, playername, number=3000):
    # Abilities
    Techn = ['Crossing', 'Dribbling', 'First Touch', 'Corners', 'Free Kick Taking', 'Technique', 'Passing', 'Left Foot',
             'Right Foot']
    Attack = ['Finishing', 'Heading', 'Long Shots', 'Penalty Taking', 'Jumping Reach']
    Power = ['Strength', 'Natural Fitness']
    Speed = ['Acceleration', 'Agility', 'Balance', 'Pace', 'Stamina']
    Defence = ['Marking', 'Tackling', 'Aggressiion', 'Long Throws', 'Foul']
    Mentality = ['Emotional control', 'Sportsmanship', 'Resistant to stress', 'Professional', 'Bravery', 'Anticipation',
                 'Composure', 'Concentration', 'Decision', 'Determination', 'Flair', 'Leadership', 'Work Rate',
                 'Teamwork', 'Stability', 'Ambition', 'Argue', 'Loyal', 'Adaptation', 'Vision', 'Off The Ball']
    GoalK = ['Reflexes', 'Kicking', 'Handling', 'One On Ones', 'Command Of Area', 'Communication', 'Eccentricity',
             'Rushing Out', 'Punching', 'Throwing', 'Aerial Reach']
    ability = Techn + Attack + Power + Speed + Defence + Mentality + GoalK
    # Corr func
    dataframe = dataframe[ability]
    corr_table = dataframe.T.corr()[[playername]].sort_values(by=playername,ascending=False)[1:number+1]
    corr_table.reset_index(inplace=True)
    corr_table.rename(columns={playername:"Correlation"}, inplace=True)
    return corr_table

similar_players=calculate_corr(df, "Paul Pogba")

def final_table(correlationtable, firstdataframe, position, nationality,maxage, minheight, maxweight):
    df2=firstdataframe.reset_index()
    final_cordf = pd.merge(similar_players, df2, on="Name")
    final_cordf = final_cordf[["Name", "Correlation", "Position.1", "Last_Player_Value", "Age", "Nationality", "Height", "Weight"]]
    final_cordf = final_cordf[final_cordf["Position.1"]==position]
    final_cordf = final_cordf[final_cordf["Age"] <= maxage]
    final_cordf = final_cordf[final_cordf["Nationality"].str.contains(nationality)]
    final_cordf = final_cordf[final_cordf["Height"] >= minheight]
    final_cordf = final_cordf[final_cordf["Weight"] <= maxweight]
    return final_cordf



finaldf=final_table(similar_players, df, "Midfielder", "Turkey",25, 180, 80)
