# Import
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import seaborn as sns
pd.set_option("display.width", 500)
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: "%.2f" % x)


# Veri Okuma / Player Database
def read_data():
    df = pd.read_excel(r"dataset\FM_2023_v2.xlsx")
    df.set_index("Name", inplace=True)
    return df

df = read_data()
df.head()

# Player Stats
def createSwot(dataframe, playername):
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
    Attributess = Techn + Attack + Power + Speed + Defence + Mentality + GoalK
    if playername in dataframe[dataframe["Position.1"] == "Goalkeeper"].index:
       dataframe1 = dataframe[dataframe.index == playername][Attributess].T.sort_values(by=playername, ascending=False).head(5)
       dataframe2 = dataframe[dataframe.index == playername][Attributess].T.sort_values(by=playername, ascending=False).tail(5)
       swot=pd.concat([dataframe1, dataframe2])
       return swot
    else:
        Attributess = [col for col in Attributess if col not in GoalK]
        dataframe1 = dataframe[dataframe.index == playername][Attributess].T.sort_values(by=playername, ascending=False).head(5)
        dataframe2 = dataframe[dataframe.index == playername][Attributess].T.sort_values(by=playername,ascending=False).tail(5)
        swot = pd.concat([dataframe1, dataframe2])
        return swot

pedri = createSwot(df, "Pedri")