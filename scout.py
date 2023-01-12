# Import
import pandas as pd
import numpy as np
import matplotlib
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.preprocessing import StandardScaler
matplotlib.use("TkAgg")
import seaborn as sns
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

### PCA ###

# Baskılama
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
        replace_with_thresholds(dataframe,i)

handle_outliers(df)

# KMeans Model

def create_kmeans(dataframe, numeric_columns):
    dataframe = dataframe[numeric_columns]
    scaler = StandardScaler()
    dataframe = pd.DataFrame(scaler.fit_transform(dataframe), columns = dataframe.columns, index=dataframe.index)
    kmeans = KMeans(random_state=1601).fit(dataframe)
    visualizer = KElbowVisualizer(kmeans, k=(1,15)).fit(dataframe)
    kmeans_final = KMeans(random_state=1601, n_clusters=visualizer.elbow_value_).fit(dataframe)
    dataframe = pd.DataFrame(scaler.inverse_transform(dataframe), columns=dataframe.columns, index=dataframe.index)
    dataframe["Clusters"] = kmeans_final.labels_
    dataframe["Clusters"] = dataframe["Clusters"]+1
    return dataframe

da = create_kmeans(df, numeric_columns=num_cols)

