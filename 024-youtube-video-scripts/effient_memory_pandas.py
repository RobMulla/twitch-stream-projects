import pandas as pd
import numpy as np

def get_dataset(size):
    # Create Fake Dataset
    df = pd.DataFrame()
    df['position'] = np.random.choice(['left','middle','right'], size)
    df['age'] = np.random.randint(1, 50, size)
    df['team'] = np.random.choice(['red','blue','yellow','green'], size)
    df['win'] = np.random.choice(['yes','no'], size)
    dates = pd.date_range('2020-01-01', '2022-12-31')
    df['date'] = np.random.choice(dates, size)
    df['prob'] = np.random.uniform(0, 1, size)
    return df

df = get_dataset(1_000)
%timeit df['age_rank'] = df.groupby(['team','size'])['age'].rank()
%timeit df['date_rank'] = df.groupby(['team','size'])['date'].rank()


df = get_dataset(1_000_000)
%timeit df['age_rank'] = df.groupby(['team','size'])['age'].rank()
%timeit df['date_rank'] = df.groupby(['team','size'])['date'].rank()
%timeit df['prob_rank'] = df.groupby(['team','size'])['prob'].rank()


df = get_dataset(1_000_000)
df['size'] = df['size'].astype('category')
%timeit df['age_rank'] = df.groupby(['team','size'])['age'].rank()
%timeit df['date_rank'] = df.groupby(['team','size'])['date'].rank()
%timeit df['prob_rank'] = df.groupby(['team','size'])['prob'].rank()


df = get_dataset(1_000_000)
df['size'] = df['size'].astype('category')
df['team'] = df['team'].astype('category')
%timeit df['age_rank'] = df.groupby(['team','size'])['age'].rank()
%timeit df['date_rank'] = df.groupby(['team','size'])['date'].rank()
%timeit df['prob_rank'] = df.groupby(['team','size'])['prob'].rank()


df = get_dataset(1_000_000)
df.info()


df = get_dataset(1_000_000)
df['size'] = df['size'].astype('category')
df['team'] = df['team'].astype('category')
df['age'] = df['age'].astype('int16')
df.info(verbose=False, show_counts=False)


df = get_dataset(1_000_000)
df['size'] = df['size'].astype('category')
df['team'] = df['team'].astype('category')
df['age'] = df['age'].astype('int16')
df['dq'] = df['dq'].map({'yes':True, 'no': False})
df['prob'] = df['prob'].astype('float16')
df.info(verbose=False, show_counts=False)


df = get_dataset(1_000_000)
df['size'] = df['size'].astype('category')
df['team'] = df['team'].astype('category')
df['age'] = df['age'].astype('int16')
%timeit df['age_rank'] = df.groupby(['team','size'])['age'].rank()
%timeit df['date_rank'] = df.groupby(['team','size'])['date'].rank()

df = get_dataset(1_000_000)
df['size'] = df['size'].astype('category')
df['team'] = df['team'].astype('category')
df['age'] = df['age'].astype('int16')
df['dq'] = df['dq'].map({'yes':True, 'no': False})
df['prob'] = df['prob'].astype('float16')
%timeit df['age_rank'] = df.groupby(['team','size'])['age'].rank()
%timeit df['date_rank'] = df.groupby(['team','size'])['date'].rank()
%timeit df['prob_rank'] = df.groupby(['team','size'])['prob'].rank()




# Datatypes
import pandas as pd
import numpy as np

def get_dataset(size):
    # Create Fake Dataset
    df = pd.DataFrame()
    df['size'] = np.random.choice(['big','medium','small'], size)
    df['age'] = np.random.randint(1, 50, size)
    df['team'] = np.random.choice(['red','blue','yellow','green'], size)
    df['win'] = np.random.choice(['yes','no'], size)
    dates = pd.date_range('2020-01-01', '2022-12-31')
    df['date'] = np.random.choice(dates, size)
    df['prob'] = np.random.uniform(0, 1, size)
    return df

def set_dtypes(df):
    df['size'] = df['size'].astype('category')
    df['team'] = df['team'].astype('category')
    df['age'] = df['age'].astype('int16')
    df['dq'] = df['dq'].map({'yes':True, 'no': False})
    df['prob'] = df['prob'].astype('float16')
    return df

df = get_dataset(1_000)
%timeit df.to_csv('test.csv')
%timeit df_csv = pd.read_csv('test.csv')

!ls -GFlash test.csv

df = get_dataset(1_000)
%timeit df.to_pickle('test.pickle')
%timeit df_pickle = pd.read_pickle('test.pickle')