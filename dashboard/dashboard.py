import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import streamlit as st
from babel.numbers import format_currency

# read data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

with st.sidebar:
    page = st.radio("Pilih Halaman:", ["Home", "Analisis"])

# Inisialisasi session state jika belum ada
if page == "Home":
    st.header(":bike: Bike Sharing Dataset :bike:")
    st.text("Dataset bike sharing siap digunakan untuk visualisasi. Terdapat dua data dalam dataset ini yaitu data peminjaman sepeda per hari dan data peminjaman sepeda per jam.")
    st.text("Data peminjaman sepeda per jam merupakan rincian dari data peminjaman sepeda per hari.")

    # maping dataframe
    hour_df["season"] = hour_df["season"].map({
        1: "Semi",
        2: "Panas",
        3: "Gugur",
        4: "Dingin"
        })

    hour_df["yr"] = hour_df["yr"].map({
        0: 2011,
        1: 2012
        })

    hour_df["mnth"] = hour_df["mnth"].map({
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

    hour_df["weekday"] = hour_df["weekday"].map({
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu"
        })

    hour_df["weathersit"] = hour_df["weathersit"].map({
        1: "Cerah",
        2: "Berawan",
        3: "Salju ringan",
        4: "Hujan deras"
        })
    
    day_df["season"] = day_df["season"].map({
        1: "Semi",
        2: "Panas",
        3: "Gugur",
        4: "Dingin"
        })

    day_df["yr"] = day_df["yr"].map({
        0: 2011,
        1: 2012
        })

    day_df["mnth"] = day_df["mnth"].map({
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

    day_df["weekday"] = day_df["weekday"].map({
        0: "Senin",
        1: "Selasa",
        2: "Rabu",
        3: "Kamis",
        4: "Jumat",
        5: "Sabtu",
        6: "Minggu"
        })

    day_df["weathersit"] = day_df["weathersit"].map({
        1: "Cerah",
        2: "Berawan",
        3: "Salju ringan",
        4: "Hujan deras"
        })

    # dataframe tabel selectbox
    yr = st.multiselect(
        "Pilih Tahun: ",
        options=hour_df["yr"].unique(),
        default=hour_df["yr"].unique()
    )
    season = st.multiselect(
        "Pilih Musim: ",
        options=hour_df["season"].unique(),
        default=hour_df["season"].unique()
    )
    df_select = hour_df.query("yr == @yr & season == @season")
    st.dataframe(df_select)

elif page == "Analisis":
    st.header("Analisis Bike Sharing Dataset :bike:")
    st.text("Berikut merupakan hasil visualisasi dari analisis dataset bike sharing yang dilakukan.")
        
    st.header("Kenaikan Jumlah Peminjaman Sepeda Per Tahun")
    # 1 line chart
    byear_df = day_df.groupby(by="yr").agg({
        "instant" : "nunique",
        "cnt" : "sum"
    }).reset_index()

    byear_df["yr"] = byear_df["yr"].map({0: 2011, 1: 2012})

    fig_yr = plt.figure(figsize=(8, 5))
    sns.lineplot(data=byear_df, x="yr", y="cnt", marker="o", label="Total Peminjaman")

    plt.ticklabel_format(style='plain', axis='y')
    plt.xticks([2011, 2012])

    plt.title("Kenaikan Jumlah Peminjaman Sepeda Per Tahun")
    plt.xlabel("Tahun")
    plt.ylabel(None)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    st.pyplot(fig_yr)
    st.markdown("Terjadi kenaikan jumlah peminjaman sepeda dari tahun 2011 sebanyak 1.243.103 menjadi 2.049.576 pada tahun 2012.")

    st.header("Jumlah Peminjaman Sepeda Berdasarkan Cuaca")
    # 2 bar chart
    # untuk cuaca hujan lebat jumlahnya sedikit jadi tidak terlihat bar nya
    hour_df["weathersit"] = hour_df["weathersit"].map({
        1: "Cerah",
        2: "Berawan",
        3: "Salju ringan",
        4: "Hujan deras",
        })
    
    weathersit = st.multiselect(
        "Pilih Cuaca: ",
        options=hour_df["weathersit"].unique(),
        default=hour_df["weathersit"].unique()
    )

    df_select = hour_df.query("weathersit == @weathersit")

    byweather = df_select.groupby(by="weathersit").sum()[["cnt"]].sort_values(by="cnt")

    fig_weather, ax = plt.subplots()
    ax.barh(byweather.index, byweather["cnt"], color = "#B7B1F2")
    plt.xlabel("Jumlah Peminjaman")
    plt.ticklabel_format(style='plain', axis='x')
    plt.tick_params(axis='y', labelsize=12)
    st.pyplot(fig_weather)
    st.markdown("Ternyata pengaruh cuaca dapat membuat perbedaan yang siginifikan terkait jumlah peminjaman sepeda, dimana cuaca cerah menjadi favorit bagi orang-orang untuk bersepeda dengan jumlah paling banyak yaitu 2.338.173 dan yang paling sedikit pada cuaca hujan deras sebanyak 223.")

    st.header("Jumlah Peminjaman Sepeda Berdasarkan Musim")
    # 3 bar chart
    byseason_df = hour_df.groupby(by="season").agg({
        "casual" : "sum",
        "registered" : "sum",
        "cnt" : "sum"
    }).reset_index()

    byseason_df["season"] = byseason_df["season"].map({
        1: "Semi",
        2: "Panas",
        3: "Gugur",
        4: "Dingin"
    })

    fig_ss = plt.figure(figsize=(10, 5))
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

    st.pyplot(fig_ss)
    st.markdown("Terdapat perbedaan jumlah peminjaman sepeda pada musim semi sebanyak 471.348 menjadi jumlah peminjaman terendah dan tertinggi yaitu musim gugur sebanyak 1.061.129.")
