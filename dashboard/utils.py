import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_style("whitegrid")
plt.style.use('fivethirtyeight')

int_to_season = {
    1:'Spring',
    2:'Summer',
    3:'Fall',
    4:'Winter',
}

int_to_month = {
    1: 'Jan', 2: 'Feb', 3: 'Mar',
    4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep',
    10: 'Oct', 11: 'Nov', 12: 'Dec',
}

int_to_year = {
    0: 2011,
    1: 2012
}

def preprocess_df(df):
    df = df.copy()
    
    df['yr'] = df['yr'].apply(lambda x : str(int_to_year[x]))
    df['mnth'] = df['mnth'].apply(lambda x : str(int_to_month[x]))
    df['season'] = df['season'].apply(lambda x : str(int_to_season[x]))
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    return df
    
def filter_df(df, date, time=None):
    df = df.copy()
    
    df = df.loc[df['dteday'] >= str(date[0])]
    if len(date) > 1:
        df = df.loc[df['dteday'] <= str(date[1])]
        
    if time is not None:
        df = df[df['hr'] >= time[0].hour]
        df = df[df['hr'] <= time[1].hour]
    
    return df

def group_bar(df:pd.DataFrame, by='hr', col='cnt'):
  df = df.copy()
  df = df.groupby(by).mean(numeric_only=True)[col]

  plot = sns.barplot(df)
  plot.set_xlabel(by)
  plot.set_ylabel("Average Count")

  return plot

def group_pie(df:pd.DataFrame, by='season', col='cnt'):
  df = df.copy()
  df = df.groupby(by).mean(numeric_only=True)[col]

  fig, ax = plt.subplots()
  ax.pie(df, labels=df.index, autopct='%.0f%%')
  return fig

def monthly_bar(df:pd.DataFrame, col='cnt', return_df=False):
  df = df.copy()
  df.sort_values(['yr', 'mnth'], inplace=True)
  df['yr_mnth'] = df['mnth']  + ', ' + df['yr']

  df_mnth_col = df.groupby('yr_mnth').mean(numeric_only=True)[col]
  df[f'mnth_{col}'] = df['yr_mnth'].apply(lambda x : df_mnth_col[x])
  df_result = df[['yr_mnth', f'mnth_{col}']].set_index('yr_mnth')
  # return df_result

  if return_df:
    return df_result

  barplot = sns.barplot(df_result[f'mnth_{col}'])
  barplot.tick_params(axis='x', rotation=90)
  
  return barplot