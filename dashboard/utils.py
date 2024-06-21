import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
plt.style.use('fivethirtyeight')

int_to_season = {
    1: 'Spring',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter',
}

def preprocess_df(df):
    df = df.copy()
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

def merge_data(day_data, hour_data):
    day_data = day_data.copy()
    hour_data = hour_data.copy()

    day_measure = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
    day_measure_dict = {x: f"{x}_day" for x in day_measure}
    day_data.rename(columns=day_measure_dict, inplace=True)

    drop_measure = [x for x in day_data.columns if x not in day_measure_dict.values()]
    drop_measure.remove('dteday')
    day_data.drop(drop_measure, axis=1, inplace=True)

    data_merge = pd.DataFrame(hour_data.merge(day_data, on="dteday", how="left"))

    return data_merge

def plot_season(data, col='cnt'):
    data = data.copy()
    data['season'] = data['season'].apply(lambda x: int_to_season[x])
    data = data.groupby('season').mean(numeric_only=True)[col]

    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct='%.0f%%', explode=[0, 0.1, 0, 0])
    return fig

def plot_user_mode_alternative(data):
    data_copy = data.copy()
    data_copy['casual_Persen'] = (data_copy['casual'] / data_copy['cnt']) * 100
    data_copy['registered_Persen'] = (data_copy['registered'] / data_copy['cnt']) * 100

    data_casual_bulanan = data_copy.groupby('mnth')['casual_Persen'].mean()
    data_registered_bulanan = data_copy.groupby('mnth')['registered_Persen'].mean()

    fig, ax = plt.subplots()
    data_casual_bulanan.plot(ax=ax, label='Casual Persen', marker='o')
    data_registered_bulanan.plot(ax=ax, label='Registered Persen', marker='o')

    ax.set_xticks(data_casual_bulanan.index)
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Persentase (%)')
    ax.legend()
    return fig

def plot_perbandingan_penyewa(data):
    data_copy = data.copy()
    perbandingan_penyewa = data_copy.groupby('workingday')['cnt'].mean()

    fig, ax = plt.subplots()
    perbandingan_penyewa.plot(kind='bar', ax=ax, color=['skyblue', 'orange'])

    ax.set_xticklabels(['Hari Kerja', 'Hari Libur'], rotation=0)
    ax.set_xlabel('Jenis Hari')
    ax.set_ylabel('Jumlah Rata-rata Penyewa Sepeda')
    ax.set_title('Perbandingan Jumlah Penyewa Sepeda pada Hari Libur dan Hari Kerja')
    return fig
