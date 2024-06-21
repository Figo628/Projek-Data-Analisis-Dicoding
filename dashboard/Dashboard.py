import streamlit as st
import pandas as pd
import numpy as np
import os
import datetime

from utils import preprocess_df, merge_data, plot_season, plot_user_mode_alternative, plot_perbandingan_penyewa

# Dapatkan direktori skrip saat ini
script_dir = os.path.dirname(os.path.abspath(__file__))

# Bangun jalur ke direktori data relatif terhadap lokasi skrip
df_dir = os.path.join(script_dir, '..', 'data')

# Bangun jalur lengkap ke file CSV
day_csv_path = os.path.join(df_dir, 'day.csv')
hour_csv_path = os.path.join(df_dir, 'hour.csv')

# Baca file CSV
df_day = pd.read_csv(day_csv_path)
df_hour = pd.read_csv(hour_csv_path)

# Preprocess data
df_day = preprocess_df(df_day)
df_hour = preprocess_df(df_hour)

# Merge data
data_merge = merge_data(df_day, df_hour)

min_date = df_day['dteday'].min()
max_date = df_day['dteday'].max()

header, _ = st.columns([0.8, 0.2])
mode_square, date_square, time_square_start, time_square_end = header.columns([10, 15, 8, 8])
mode = mode_square.radio("Select mode:", ["Daily", 'Hourly'])

if mode == "Daily":
    date = date_square.date_input(
        label='Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    df_cur = df_day[(df_day['dteday'] >= pd.to_datetime(date[0])) & (df_day['dteday'] <= pd.to_datetime(date[1]))]

    st.subheader("Plot Berdasarkan Season")
    fig_season = plot_season(df_cur)
    st.pyplot(fig_season)

    st.subheader("Plot Perbandingan Penyewa pada Hari Kerja dan Hari Libur")
    fig_perbandingan_penyewa = plot_perbandingan_penyewa(data_merge)
    st.pyplot(fig_perbandingan_penyewa)

else:
    date = date_square.date_input(
        label='Date Range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    time_start = time_square_start.time_input('Hour Start', datetime.time(0, 0))
    time_end = time_square_end.time_input('Hour End', datetime.time(23, 0))

    df_cur = df_hour[(df_hour['dteday'] >= pd.to_datetime(date[0])) & (df_hour['dteday'] <= pd.to_datetime(date[1]))]
    df_cur = df_cur[(df_cur['hr'] >= time_start.hour) & (df_cur['hr'] <= time_end.hour)]

    st.subheader("Plot Berdasarkan Mode Pengguna")
    fig_user_mode = plot_user_mode_alternative(df_cur)
    st.pyplot(fig_user_mode)

st.dataframe(df_cur)
