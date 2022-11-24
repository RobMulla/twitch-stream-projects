#!/usr/bin/env python
# coding: utf-8

# # Speed up your Pandas Code!

# In[1]:


get_ipython().run_line_magic('load_ext', 'lab_black')


# In[2]:


import pandas as pd
import numpy as np


# ## The Problem
# Looping through a pandas dataframe and creating a new column based on existing ones.

# In[3]:


np.random.randint(0, 90, 10_000).shape


# In[4]:


# Create fake data
def get_data(size=10_000):
    df = pd.DataFrame()
    df["age"] = np.random.randint(0, 100, size)
    df["time_in_bed"] = np.random.randint(0, 9, size)
    df["pct_sleeping"] = np.random.rand(size)
    df["favorite_food"] = np.random.choice(["pizza", "taco", "ice cream"], size)
    df["hate_food"] = np.random.choice(["broccoli", "candy corn", "eggs"], size)
    return df


# In[5]:


# If they sleep more than 5 hours and more than 50% in REM give favorite food
# Otherwise give them their least favorite
# Unless they are over 90 years old and give them their favorite.


# In[6]:


def reward_calc(row):
    if row["age"] >= 90:
        return row["favorite_food"]
    if (row["pct_sleeping"] > 0.5) & (row["time_in_bed"] > 5):
        return row["favorite_food"]
    return row["hate_food"]


# ## Level 1 - Loop


df = get_data()
for index, row in df.iterrows():
    df.loc[index, 'reward'] = reward_calc(row)

# ## Level 2 - Apply


%%timeit
df = get_data()
df['reward'] = df.apply(reward_calc, axis=1)


# ## Level 3 - Vectorized

%%timeit
df = get_data()
df['reward'] = df['hate_food'] 
df.loc[((df["pct_sleeping"] > 0.5) & (df["time_in_bed"] > 5)) | (df["age"] > 90), "reward"] = df["favorite_food"]

# # Results

results = pd.DataFrame(
    [
        ["loop", 3580, 48.3],
        ["apply", 192, 6.34],
        ["vectorized", 1.36, 0.00896],
    ],
    columns=["type", "mean", "std"],
)
