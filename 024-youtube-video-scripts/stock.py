!pip install fredapi > /dev/null

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import plotly.express as px
import requests
from tqdm import tqdm

from fredapi import Fred

plt.style.use('fivethirtyeight')
pd.set_option("max_columns", 500)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]

from kaggle_secrets import UserSecretsClient
secrets = UserSecretsClient()
fred_key = secrets.get_secret('fred-api')

# Create A FRED object
fred = Fred(api_key=fred_key)

sp_results = fred.search('S&P')

table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')