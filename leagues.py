import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.preprocessing import RobustScaler

    ##########! DATA PREPROCESS !##########
#TODO READ DATA, SCALING, KNNIMPUTER

df=pd.read_excel(r"dataset\FM_2023_v2.xlsx")
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
num_cols= num_cols+["GK"]


knn = KNNImputer(n_neighbors=5)
scaler = RobustScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])
df[num_cols] = pd.DataFrame(knn.fit_transform(df[num_cols]), columns=df[num_cols].columns)

df[num_cols] = pd.DataFrame(scaler.inverse_transform(df[num_cols]), columns=df[num_cols].columns)

df.to_excel("FM_2023_final.xlsx")




def value_calculation(dataframe,position):
    mevki_siralama=dataframe[dataframe["Position.1"]==position].sort_values("Last_Player_Value", ascending=False).head(10)
    mevki_siralama=mevki_siralama[["Name","Last_Player_Value"]]
    return mevki_siralama
value_calculation(df, "Forward")

midfielder_top10=value_calculation(df, "Midfielder")
forward_top10=value_calculation(df, "Forward")
defender_top10=value_calculation(df, "Defender")
goalkeeper_top10=value_calculation(df, "Goalkeeper")


League_total_value=(df.groupby("Leagues").agg({"Last_Player_Value":"sum"})).plot(kind="bar")
(df.groupby("Leagues").agg({"Last_Player_Value":"sum"})).plot(kind="bar",  color="r")
plt.show(block=True)
sns.boxplot(data=df, palette="OrRd",y="Position.1", x="Last_Player_Value")
def taktik_belirleme(dataframe,taktik):
    if  taktik=="4-4-2":
        taktik1=df[df["Position.1"]=="Forward"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(2)
        taktik2=df[df["Position.1"]=="Defender"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(4)
        taktik3=df[df["Position.1"]=="Midfielder"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(4)
        taktik4=df[df["Position.1"] == "Goalkeeper"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(1)
        taktiks = pd.concat([taktik4,taktik2,taktik3,taktik1])
        return taktiks
    elif  taktik=="3-5-2":
        taktik1=df[df["Position.1"]=="Forward"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(2)
        taktik2=df[df["Position.1"]=="Defender"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(3)
        taktik3=df[df["Position.1"]=="Midfielder"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(5)
        taktik4=df[df["Position.1"] == "Goalkeeper"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(1)
        taktiks = pd.concat([taktik4, taktik2, taktik3, taktik1])
        return taktiks
    elif taktik=="4-3-3":
       taktik1=df[df["Position.1"] == "Forward"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(3)
       taktik2=df[df["Position.1"] == "Defender"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(4)
       taktik3=df[df["Position.1"] == "Midfielder"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(3)
       taktik4=df[df["Position.1"] == "Goalkeeper"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(1)
       taktiks = pd.concat([taktik4, taktik2, taktik3, taktik1])
       return taktiks
    else:
       taktik1=df[df["Position.1"] == "Forward"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(1)
       taktik2=df[df["Position.1"] == "Defender"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(4)
       taktik3=df[df["Position.1"] == "Midfielder"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(5)
       taktik4=df[df["Position.1"] == "Goalkeeper"].sort_values("Last_Player_Value", ascending=False)[["Name","Position.1","Club"]].head(1)
       taktiks = pd.concat([taktik4, taktik2, taktik3, taktik1])
       return taktiks

taktik_belirleme(df,"4-3-3")



taktik_belirleme=pd.DataFrame(taktik_belirleme(df, "3-5-2"))
taktik_belirleme2=taktik_belirleme(df, "4-3-3")
taktik_belirleme3=taktik_belirleme(df,"4-4-2")
taktik_belirleme1=taktik_belirleme(df,"3-5-2")


taktik_belirleme.to_excel("taktik_belirleme_ucbesiki.xlsx")

