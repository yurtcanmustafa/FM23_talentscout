import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform, pdist
import seaborn as sns
from soccerplots.radar_chart import Radar
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)

#* PLAYERS => 
df = pd.read_excel(r"FM_2023_final.xlsx")
df.head()

def grab_col_names(dataframe, cat_th=10,  car_th=20):
    """
    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.

    Parameters
    ----------
    dataframe: dataframe
        değişken isimleri alınmak istenen dataframe'dir.
    cat_th: int, float
        numerik fakat kategorik olan değişkenler için sınıf eşik değeri
    car_th: int, float
        kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    -------
    cat_cols: list
        Kategorik değişken listesi
    num_cols: list
        Numerik değişken listesi
    cat_but_car: list
        Kategorik görünümlü kardinal değişken listesi

    Notes
    ------
    cat_cols + num_cols + cat_but_car = toplam değişken sayısı
    num_but_cat cat_cols'un içerisinde.

    """
    # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if str(dataframe[col].dtypes) in ["category", "object", "bool"]]

    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and dataframe[col].dtypes in ["int64", "float64"]]

    cat_but_car = [col for col in dataframe.columns if
                   dataframe[col].nunique() > car_th and str(dataframe[col].dtypes) in ["category", "object"]]

    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes in ["int64", "float64"]]
    num_cols = [col for col in num_cols if col not in cat_cols]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')

    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df)

#? Oyuncu kıyaslama
player_columns = ["Age", "Last_Player_Value", "Salary", "Nationality"]

def player_compare(dataframe, player1, player2, columns):
    compared_df = dataframe.loc[(dataframe["Name"] == player1) | (dataframe["Name"] == player2), columns]
    return compared_df

player_compare(dataframe=df, player1="Pedri", player2="Harry Kane", columns=player_columns)

pedri = df.loc[df["Name"] == "Pedri" , player_columns]
kane = df.loc[df["Name"] == "Harry Kane" , player_columns]

#? Radar Graph
def radar_graph(dataframe, plot=False):
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

    dataframe["Techn"] = dataframe[Techn].apply(lambda x: x.mean(), axis=1)
    dataframe["Attack"] = dataframe[Attack].apply(lambda x: x.mean(), axis=1)
    dataframe["Power"] = dataframe[Power].apply(lambda x: x.mean(), axis=1)
    dataframe["Speed"] = dataframe[Speed].apply(lambda x: x.mean(), axis=1)
    dataframe["Mentality"] = dataframe[Mentality].apply(lambda x: x.mean(), axis=1)
    dataframe["GoalK"] = dataframe[GoalK].apply(lambda x: x.mean(), axis=1)
    grouped_attributes = ["Techn", "Attack", "Power", "Speed", "Mentality", "GoalK"]
    radar_plot = ["Name"] + grouped_attributes
    df_radar = dataframe[radar_plot]
    return df_radar
    if plot:
        df_radar.to_excel("radar_plot.xlsx")

radar = radar_graph(df)
def create_radarchart(dataframe, player1, player2):
    dataframe.set_index("Name", inplace=True)
    params = list(dataframe.columns)
    dfradar = dataframe.reset_index()
    ranges = []
    a_values = []
    b_values = []
    for x in params:
        a = min(dfradar[params][x])
        a = a - (a * .25)

        b = max(dfradar[params][x])
        b = b + (b * .25)
        ranges.append((a, b))
    for x in range(len(dfradar["Name"])):
        if dfradar["Name"][x] == player1:
            a_values = dfradar.iloc[x].values.tolist()
        if dfradar["Name"][x] == player2:
            b_values = dfradar.iloc[x].values.tolist()

    a_values = a_values[1:]
    b_values = b_values[1:]
    values = [a_values, b_values]
    title = dict(
        title_name=player1,
        title_color="green",
        title_name_2=player2,
        title_color_2="red",
        title_fontsize=18)
    radar = Radar()
    fig, ax = radar.plot_radar(ranges=ranges, params=params, values=values, radar_color=["green", "red"],
                               alphas=[.5, .3], title=title, compare=True)
    plt.show(block=True)
    dataframe.reset_index(inplace=True)


create_radarchart(radar, "Cristiano Ronaldo", "Erling Haaland")

#! Bar Plot
def barplot(dataframe, plot=False):
    Techn = ['Crossing', 'Dribbling', 'First Touch', 'Corners', 'Free Kick Taking', 'Technique', 'Passing', 'Left Foot',
             'Right Foot']
    Attack = ['Finishing', 'Heading', 'Long Shots', 'Penalty Taking', 'Jumping Reach']
    Power = ['Strength', 'Natural Fitness']
    Speed = ['Acceleration', 'Agility', 'Balance', 'Pace', 'Stamina']
    Defence = ['Marking', 'Tackling', 'Aggressiion', 'Long Throws', 'Foul']
    Mentality = ['Emotional control', 'Sportsmanship', 'Resistant to stress', 'Professional', 'Bravery', 'Anticipation',
                 'Composure', 'Concentration', 'Decision', 'Determination', 'Flair', 'Leadership', 'Work Rate',
                 'Teamwork', 'Stability', 'Ambition', 'Argue', 'Loyal', 'Adaptation', 'Vision', 'Off The Ball']
    barplot_attributes = ["Name"] + Techn + Attack + Power + Speed + Defence + Mentality
    barplot = dataframe[barplot_attributes]
    barplot.set_index("Name", inplace=True)
    return barplot
    if plot:
        barplot.to_excel("barplot.xlsx")

barplot = barplot(df)

def barplot_graphic(dataframe, player1, player2):
    barplott=barplot(dataframe)
    plt.figure(figsize=(25, 8))
    plt.subplot(1, 2, 1)
    plt.title(f"{player1}")
    chart = sns.barplot(data=barplott[barplott.index == player1], palette="Set3")
    chart.set_xticklabels(chart.get_xticklabels(), rotation=90)
    plt.subplot(1, 2, 2)
    plt.title(f"player2")
    chart2 = sns.barplot(data=barplott[barplott.index == player2], palette="Set3")
    chart2.set_xticklabels(chart2.get_xticklabels(), rotation=90)
    plt.show()

barplot_graphic(df, "Cristiano Ronaldo", "Erling Haaland")

#! Similarity
def similarity_df(dataframe):
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
    position = ["DL", "DC", "DR", "WBL", "WBR", "DM", "ML", "MC", "MR", "AML", "AMC", "AMR", "ST", "GK"]
    similarity_cols = ["Name"] + Techn + Attack + Power + Speed + Defence + Mentality + GoalK + position
    similarity = dataframe[similarity_cols]
    similarity.set_index("Name", inplace=True)
    return similarity

df2 = similarity_df(df)

#* Euclidean Distance
distances = pdist(df2, metric="euclidean")
dist_matrix = squareform(distances)
euclidean_distance = pd.DataFrame(dist_matrix, columns=df2.index, index=df2.index)
euclidean_distance.to_excel("euclidean_distance.xlsx")
euclidean_distance.iloc[0:5, 0:5]

#* Canberra Distance
canberra_distances = pdist(df2, metric="canberra")
canberradist_matrix = squareform(canberra_distances)
canberradistance = pd.DataFrame(canberradist_matrix, columns=df2.index, index=df2.index)
canberradistance.to_excel("canberradistance.xlsx")
euclidean_distance.iloc[0:5, 0:5]


#* Minkowski Distance
minkowski_distance = pdist(df2, metric="minkowski")
minkowski_matrix = squareform(minkowski_distance)
minkowskidistance = pd.DataFrame(minkowski_matrix, columns=df2.index, index=df2.index)
minkowskidistance.to_excel("minkowskidistance.xlsx")


#* Correlation Distance
correlation_distance = pdist(df2, metric="correlation")
correlation_matrix = squareform(correlation_distance)
correlationdistance = pd.DataFrame(correlation_matrix, columns=df2.index, index=df2.index)
correlationdistance.to_excel("correlationdistance.xlsx")


#* cityblock(manhattan) distance
cityblock_distance = pdist(df2, metric="cityblock")
cityblock_matrix = squareform(cityblock_distance)
cityblockdistance = pd.DataFrame(cityblock_matrix, columns=df2.index, index=df2.index)
cityblockdistance.to_excel("cityblockdistance.xlsx")


#* jaccard distance
jaccard_distance = pdist(df2, metric="jaccard")
jaccard_matrix = squareform(jaccard_distance)
jaccarddistance = pd.DataFrame(jaccard_matrix, columns=df2.index, index=df2.index)
jaccarddistance.to_excel("jaccarddistance.xlsx")

def create_distance(dataframe, metric, plot=False):
    from scipy.spatial.distance import pdist, squareform
    distance = pdist(dataframe, metric=metric)
    matrix = squareform(distance)
    distance_df = pd.DataFrame(matrix, columns=dataframe.index, index=dataframe.index)
    return distance_df
    if plot:
        distance_df.to_excel(f"{metric}_distance.xlsx")

# En benzeyen 5 kişi
def most_similar(dataframe, number=5):
    euc_list={}
    for i in list(dataframe.columns):
        euc_list.update({i:list(dataframe[i].sort_values(ascending=True)[1:number+1].index)})
    ec=pd.DataFrame(euc_list)
    return ec
