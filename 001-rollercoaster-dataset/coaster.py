import pandas as pd

def parse_coaster_infobox(url, coaster_name, filter_cols=False):
    """
    Takes a coaster wikipedia url.
    Pulls info from the infobox and returns as a dataframe
    """
    try:
        df = pd.read_html(url, attrs= {'class': 'infobox'})[0]
    except ValueError:
        return pd.DataFrame()

    mycoaster = df.columns[0]
    df = df[df.columns[:2]]
    df.columns = ['Coaster', 'Value']
    df = df.set_index('Coaster')
    df = df.loc[~df.index.isna()]
    if filter_cols:
        MAIN_KEYS = ['coaster_name', 'Length', 'Speed', 'Location', 'Coordinates',
                     'Status', 'Opening date',
                     'General statistics', 'Type', 'Manufacturer',
                     'Height restriction',
                     'Model', 'Height', 'Inversions', 'Lift/launch system',
                     'Cost', 'Trains',
                     'Park section', 'Duration', 'Capacity',
                     'G-force', 'Designer',
                     'Max vertical angle', 'Drop', 'Soft opening date',
                     'Fast Lane available', 'Replaced', 'Track layout',
                     'Fastrack available','Soft opening date',
                     'Closing date', 'Opened', 'Replaced by', 'General Statistics',
                     'Website', 'Flash Pass Available', 'Must transfer from wheelchair',
                     'Theme', 'Single rider line available',
                     'Restraint Style',
                      'Flash Pass available', 'Acceleration',
                      'Restraints', 'Name']

        FILTERED_KEYS = [v for v in df.index if v in MAIN_KEYS]
        df = df.loc[FILTERED_KEYS]
    df = df.T
    df.index = [mycoaster]
    df = dedup_infobox(df)
    df['coaster_name'] = coaster_name
    return df

def dedup_infobox(df):
    dup_cols = df.columns[df.columns.duplicated()].unique()
    for c in dup_cols:
        cols = []
        count = 1
        for column in df.columns:
            if column == c:
                cols.append(f'{c}_{count}')
                count+=1
                continue
            cols.append(column)
        df.columns = cols
    return df
