import pandas as pd
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

player_columns = ["Age", "Last_Player_Value", "Salary", "Nationality"]

df.head()

#? Oyuncu kıyaslama
pedri = df.loc[df["Name"] == "Pedri" , player_columns]
kane = df.loc[df["Name"] == "Harry Kane" , player_columns]

#? Radar Graph


Technique = ['Crossing',  'Dribbling', 'First Touch', 'Corners', 'Free Kick Taking', 'Technique', 'Passing', 'Left Foot', 'Right Foot']
Attack = ['Finishing', 'Heading', 'Long Shots', 'Penalty Taking', 'Jumping Reach']
Power = ['Strength', 'Natural Fitness']
Speed = ['Acceleration', 'Agility', 'Balance', 'Pace', 'Stamina']
Defence = ['Marking', 'Tackling', 'Aggressiion', 'Long Throws', 'Foul']
Mentality = ['Emotional control', 'Sportsmanship', 'Resistant to stress', 'Professional', 'Bravery', 'Anticipation', 'Composure', 'Concentration', 'Decision', 'Determination', 'Flair', 'Leadership', 'Work Rate', 'Teamwork', 'Stability', 'Ambition', 'Argue', 'Loyal', 'Adaptation', 'Vision', 'Off The Ball']
GoalK = ['Reflexes', 'Kicking', 'Handling', 'One On Ones',  'Command Of Area', 'Communication', 'Eccentricity', 'Rushing Out', 'Punching', 'Throwing', 'Aerial Reach']

df["Technique"] = df[Technique].apply(lambda x: x.mean(), axis=1)
df["Attack"] = df[Attack].apply(lambda x: x.mean(), axis=1)
df["Power"] = df[Power].apply(lambda x: x.mean(), axis=1)
df["Speed"] = df[Speed].apply(lambda x: x.mean(), axis=1)
df["Mentality"] = df[Mentality].apply(lambda x: x.mean(), axis=1)
df["GoalK"] = df[GoalK].apply(lambda x: x.mean(), axis=1)

grouped_attributes = ["Technique","Attack","Power", "Speed", "Mentality" ,"GoalK"]
radar_plot = ["Name"] + grouped_attributes
df_radar = df[radar_plot] 
df_radar.to_excel("radar_plot.xlsx")
