# TQDM is awesome

%load_ext lab_black

import pandas as pd
import numpy as np
from tqdm import tqdm, trange
from time import sleep

# Fake data
dogs = np.random.choice(['labradoodle','beagle', 'mutt'], size=50_000)
smell = np.random.randint(0, 100, size=50_000)
df = pd.DataFrame(data=np.array([dogs,smell]).T, columns=['dog','smell'])

text = ""
for char in tqdm(["a", "b", "c", "d"]):
    sleep(0.25)
    text = text + char

# Basic loop
for i in trange(100):
    sleep(0.01)

# Manually setting size
for i in tqdm(mylist, total=5):
    sleep(0.01)

## On while loop
pbar = tqdm(total=50_000)
for s in smell:
    pbar.update(1)
    sleep(0.00001)
pbar.close()


## Setting a Description and unit
for i in trange(100, desc="hello", unit="epoch"):
    sleep(0.01)


## Nested Progress
for i in trange(4, desc='1st loop'):
    for j in trange(5, desc='2nd loop'):
        sleep(0.01)


for dog in tqdm(dogs[:5], desc='dog counter', total=5):
    for s in tqdm(smell[:2], desc='smell counter', total=2):
        sleep(0.1)

## Dynamic Description

pbar = tqdm(dogs[:10])
for dog in pbar:
    sleep(0.5)
    pbar.set_description(f"Processing {dog}")


# Controlling Size
#Resizing to 55 columns; Progress bar is shortened
for i in tqdm(range(9999999), ncols=55):
    pass
#Further resizing; Time stats are taken out
for i in tqdm(range(9999999), ncols=20):
    pass
#Progress is shown only as %
for i in tqdm(range(9999999), ncols=4):
    pass

#  intervals
for dog in tqdm(dogs, mininterval=1):
    sleep(0.00001)
    
for dog in tqdm(dogs, maxinterval=10):
    sleep(0.00001)


## Disabling progress bar
debug = False
for i in tqdm(range(0, 100), disable=not debug): 
    sleep(.01) 
print("Done") 

## Custom `bar_format`
```
Possible vars:
l_bar, bar, r_bar, n, n_fmt, total, total_fmt,
 |            percentage, elapsed, elapsed_s, ncols, nrows, desc, unit,
 |            rate, rate_fmt, rate_noinv, rate_noinv_fmt,
 |            rate_inv, rate_inv_fmt, postfix, unit_divisor,
 |            remaining, remaining_s, eta.
```
## Nested progress bars


for i in trange(4, desc='1st loop'):
    for j in trange(5, desc='2nd loop'):
        for k in trange(50, desc='3nd loop', leave=False):
            sleep(0.01)


# TQDM + Pandas = ❤️


df = pd.DataFrame(np.random.randint(0, 100, (100000, 6)))

tqdm.pandas(desc="my bar!")

out = df.progress_apply(lambda x: x**2)
out = df.groupby(0).progress_apply(lambda x: x**2)


tqdm.pandas(desc='my bar')

df.progress_apply(lambda row: row['smell']**2, axis=1)

# TQDM in Notebook

from tqdm.notebook import tqdm
text = ""
for char in tqdm(["a", "b", "c", "d"]):
    sleep(0.25)
    text = text + char

## Red Progress bar on failure

counter = 0
for dog in tqdm(dogs):
    if dog == 'beagle':
        counter += 1
    if counter == 10_000:
        break
        

## TQDM auto
from tqdm.auto import tqdm

## Used in command line
! seq 9999999 | python3 -m tqdm --bytes | wc -l


Why?
Easy
Quick
- <100ns per iteration overhead
- Unit tested against performance regression
- Skips unnecessary iteration displays (no console spamming)

Intelligent ETA (remaining time)
Cross-platform (Linux, Windows, Mac, FreeBSD, NetBSD, Solaris/SunOS)
Console, terminal, GUI, IPython/Jupyter
Dependency-free

help(tqdm)