import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

df = pd.read_excel("/content/drive/MyDrive/Bitirme Projesi_012023/KNN'li Data/FM_2023_final.xlsx")

df.head()

##Summary##
df.groupby(["Position.1"]).agg({"Crossing": "mean",
                                "Dribbling": "mean",
                                "Finishing": "mean",
                                "Heading": "mean",
                                "Long Shots": "mean",
                                "Long Throws": "mean",
                                "Marking": "mean",
                                "Passing": "mean",
                                "Penalty Taking": "mean",
                                "Technique": "mean",
                                "Bravery": "mean",
                                "Concentration": "mean",
                                "Vision": "mean",
                                "Leadership": "mean",
                                "Teamwork": "mean",
                                "Acceleration": "mean",
                                "Stamina": "mean",
                                "Adaptation": "mean",
                                "Sportsmanship": "mean",
                                "Emotional control": "mean"})

##Value##

def team_best(dataframe, variable1, variable2):
    team_best = dataframe.loc[(dataframe["Leagues"] == variable1) & (dataframe["Club"] == variable2)]
    best_ten_player = team_best.sort_values("Last_Player_Value", ascending=False).head(10)
    player_name = best_ten_player[["Name"]]
    return player_name


team_best(df, "LaLiga", "Barcelona")


# Baskılama
def grab_col_names(dataframe, cat_th=10, car_th=20):
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
    num_but_cat = [col for col in dataframe.columns if
                   dataframe[col].nunique() < cat_th and dataframe[col].dtypes in ["int64", "float64"]]
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

def outlier_thresholds(dataframe, col_name, q1=0.05, q3=0.95):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def check_outlier(dataframe, col_name):
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
        return True
    else:
        return False

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


def handle_outliers(dataframe):
    outlier_cols = []
    for col in num_cols:
        if check_outlier(df, col):
            outlier_cols.append(col)
    for i in outlier_cols:
        replace_with_thresholds(dataframe, i)

handle_outliers(df)

##Boxplot##
sns.boxplot(data=df, x="Position.1", y="Last_Player_Value")

df2 = df[df["Position.1"] == "Defender"]

##Kdeplot##
sns.kdeplot(data=df2, x="Last_Player_Value")

##Stats##
def team_statistics(dataframe, league, team):
    Oldest_Player = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Age", ascending=False)[
        "Name"].head(1).values
    print("Oldest Player:", Oldest_Player)
    Youngest_Player = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Age", ascending=False)[
        "Name"].tail(1).values
    print("Youngest_Player:", Youngest_Player)
    Most_Valuable_Player = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Last_Player_Value",
                                                                                              ascending=False)[
        "Name"].head(1).values
    print("Most_Valuable_Player:", Most_Valuable_Player)
    Best_Penalty_Taker = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Penalty Taking",
                                                                                              ascending=False)[
        "Name"].head(1).values
    print("Best_Penalty_Taker:", Best_Penalty_Taker)
    Best_Freekick_Taker = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Free Kick Taking",
                                                                                              ascending=False)[
        "Name"].head(1).values
    print("Best_Freekick_Taker:", Best_Freekick_Taker)
    Best_Leadership = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Leadership",
                                                                                              ascending=False)[
        "Name"].head(1).values
    print("Best_Leadership:", Best_Leadership)

    Best_Finishing = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Finishing",
                                                                                              ascending=False)[
        "Name"].head(1).values
    print("Best_Finishing:", Best_Finishing)
    Best_Technique = \
    dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)].sort_values("Technique",
                                                                                              ascending=False)[
        "Name"].head(1).values
    print("Best_Technique:", Best_Technique)

team_statistics(df, "LaLiga", "Barcelona")

##SetPieceGoal##
def set_piece_goal(dataframe, league, team):
    league_team_select = dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)]
    free_kick_takers = league_team_select.sort_values("Free Kick Taking", ascending=False).head(10)
    best_free_kick_takers = free_kick_takers["Name"]
    print("Free Kick Takers:", "\n", best_free_kick_takers)
    penalty_takers = league_team_select.sort_values("Penalty Taking", ascending=False).head(10)
    best_penalty_takers = penalty_takers["Name"]
    print("Penalty Takers", "\n", best_penalty_takers)

set_piece_goal(df, "LaLiga", "Barcelona")

##BMI##
def bmi(dataframe, league, team):
    league_team_select = dataframe.loc[(dataframe["Leagues"] == league) & (dataframe["Club"] == team)]
    bmi_best = league_team_select.sort_values("BMI%", ascending=False).head(10)
    bmi_best_name = bmi_best[["Name", "BMI%"]]
    bmi_worst = league_team_select.sort_values("BMI%", ascending=False).tail(10)
    bmi_worst_name = bmi_worst[["Name", "BMI%"]]
    print("BMI% Best 10 Player:", "\n", bmi_best_name, "\n", "BMI% Worst 10 Player:", "\n", bmi_worst_name)


bmi(df, "Süper Lig", "Fenerbahçe A.Ş.")