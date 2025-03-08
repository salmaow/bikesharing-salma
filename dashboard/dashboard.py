import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from streamlit_option_menu import option_menu

# read data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# header
st.header(":bike: Bike Sharing Dataset :bike:")

# main
st.text("Dataset bike sharing siap digunakan untuk visualisasi. Terdapat dua data dalam dataset ini yaitu data peminjaman sepeda per hari dan data peminjaman sepeda per jam yang dapat dilihat pada tabel berikut.")

# sidebar menu
with st.sidebar:
    st.button("Home", "dashboard/dashboard.py")


# tampilkan tabel day_df dan replace isi data
st.write("Data Peminjaman Sepeda Per Hari")

# ambil dan simpan data di session state
if "day_df.replace" not in st.session_state:
    st.session_state["day_df.replace"] = "day_df"

day_df["season"] = day_df["season"].replace({
        1: "Semi",
        2: "Panas",
        3: "Gugur",
        4: "Dingin"
})

day_df["yr"] = day_df["yr"].replace({
    0: "2011",
    1: "2012",
})

day_df["mnth"] = day_df["mnth"].replace({
    1: "Jan",
    2: "Feb",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Ags",
    9: "Sept",
    10: "Okt",
    11: "Nov",
    12: "Des"
})

day_df["weekday"] = day_df["weekday"].replace({
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu"
})

day_df["weathersit"] = day_df["weathersit"].replace({
    1: "Cerah",
    2: "Berawan",
    3: "Salju ringan",
    4: "Hujan deras",
})

st.dataframe(day_df)


# tampilkan tabel day_df dan replace isi data
st.write("Data Peminjaman Sepeda Per Jam")

if "hour_df.replace" not in st.session_state:
    st.session_state["hour_df.replace"] = "hour_df"
 
hour_df["season"] = hour_df["season"].replace({
        1: "Semi",
        2: "Panas",
        3: "Gugur",
        4: "Dingin"
})

hour_df["yr"] = hour_df["yr"].replace({
    0: "2011",
    1: "2012",
})

hour_df["mnth"] = hour_df["mnth"].replace({
    1: "Jan",
    2: "Feb",
    3: "Maret",
    4: "April",
    5: "Mei",
    6: "Juni",
    7: "Juli",
    8: "Ags",
    9: "Sept",
    10: "Okt",
    11: "Nov",
    12: "Des"
})

hour_df["weekday"] = hour_df["weekday"].replace({
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Minggu"
})

hour_df["weathersit"] = hour_df["weathersit"].replace({
    1: "Cerah",
    2: "Berawan",
    3: "Salju ringan",
    4: "Hujan deras",
})
st.dataframe(hour_df)

def create_byear_df(df):
    byear_df = day_df.groupby(by="yr").agg({
        "instant" : "nunique",
        "cnt" : "sum"
    }).reset_index()
    
    return byear_df

def create_bweather_df(df):
    byweather_df = hour_df.groupby(by="weathersit").cnt.sum().reset_index()
    
    return byweather_df

def create_byseason_df(df):
    byseason_df = hour_df.groupby(by="season").agg({
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum"
    }).reset_index()

    return byseason_df

# main_df = day_hour_df

# byear_df = create_byear_df(main_df)
# bweather_df = create_bweather_df(main_df)
# byseason_df = create_byseason_df(main_df)

st.header("Kenaikan Jumlah Peminjaman Sepeda Per Tahun")
# 1 line chart
byear_df = day_df.groupby(by="yr").agg({
    "instant" : "nunique",
    "cnt" : "sum"
}).reset_index()

fig = plt.figure(figsize=(8, 5))
sns.lineplot(data=byear_df, x="yr", y="cnt", marker="o", label="Total Peminjaman")

plt.ticklabel_format(style='plain', axis='y')
plt.xticks(["2011", "2012"])

plt.title("Kenaikan Jumlah Peminjaman Sepeda Per Tahun")
plt.xlabel("Tahun")
plt.ylabel(None)
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()

st.pyplot(fig)
st.text("Kesimpulannya terdapan kenaikan jumlah peminjaman sepeda dari tahun 2011 ke tahun 2012.")

st.header("Jumlah Peminjaman Sepeda Berdasarkan Musim")
# 2 bar chart
# untuk cuaca hujan lebat jumlahnya sedikit jadi tidak terlihat bar nya
byweather_df = hour_df.groupby(by="weathersit").cnt.sum().reset_index()

fig = plt.figure(figsize=(10, 5))
colors_ = ["#D5E5D5", "#D5E5D5", "#B7B1F2", "#D5E5D5"]
sns.barplot(
    y="weathersit", 
    x="cnt",
    data=byweather_df.sort_values(by="weathersit", ascending=False),
    hue="weathersit",
    palette=colors_
)

plt.title("Jumlah Peminjaman Sepeda Berdasarkan Cuaca", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel("Jumlah Peminjaman")
plt.ticklabel_format(style='plain', axis='x')
plt.tick_params(axis='y', labelsize=12)

st.pyplot(fig)
st.text("Pengaruh cuaca membuat perbedaan yang signifikan terkait jumlah peminjaman sepeda, dimana cuaca cerah menjadi cuara terfavorit untuk bersepeda.")

st.header("Jumlah Peminjaman Sepeda Berdasarkan Musim")
# 3 bar chart
byseason_df = hour_df.groupby(by="season").agg({
    "casual" : "sum",
    "registered" : "sum",
    "cnt" : "sum"
}).reset_index()

fig = plt.figure(figsize=(10, 5))
colors_ = ["#B7B1F2", "#FFDCCC", "#FFDCCC", "#FFDCCC"]
sns.barplot(
    y="season",
    x="cnt",
    data=byseason_df.sort_values(by="season", ascending=False),
    hue="season",
    palette=colors_
)

plt.title("Jumlah Peminjaman Berdasarkan Musim", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel("Jumlah Peminjaman")
plt.ticklabel_format(style='plain', axis='x')
plt.tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.text(" Perubahan musim juga berpengaruh bagi jumlah peminjaman sepeda, bisa dilihat ternyata jumlah peminjaman sepeda paling sedikit ada di musim semi.")
