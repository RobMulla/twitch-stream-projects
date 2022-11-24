import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from glob import glob

import librosa
import librosa.display
import IPython.display as ipd

from itertools import cycle

sns.set_theme(style="white", palette=None)
color_pal = plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])

BASE_DIR = '../input/ravdess-emotional-speech-audio/'
audio_files = glob(f'{BASE_DIR}/*/*.wav')



# Play Audio
ipd.Audio(audio_files[0])

# Loading in audio data
y, sr = librosa.load(audio_files[0])

print(f'y: {y:10}')
print(f'y shape: {y.shape}')
print(f'Sample Rate (KHz) {sr}:')

# Plot Audio
pd.Series(y).plot(figsize=(10, 5), lw=1, title='Raw Audio Data')
plt.show()

# Trim and plot
# zoom in plot

y_trimmed, _ = librosa.effects.trim(y, top_db=20)
pd.Series(y_trimmed).plot(figsize=(10, 5), lw=1, color=color_pal[1], title='Trimmed Raw Audio')


# zoom in plot
pd.Series(y[20000:55000]).plot(figsize=(10, 5), lw=1, color=color_pal[1])

# zoom wayyyy in
pd.Series(y[20000:21000]).plot(figsize=(10, 5), lw=1, color=color_pal[1])


# Spectogram

D = librosa.stft(y)  # STFT of y
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)


fig, ax = plt.subplots(figsize=(10, 5))
img = librosa.display.specshow(S_db, 
                               x_axis='time',
                               y_axis='log',
                               ax=ax)
ax.set_title('Spectogram Example', fontsize=20)
fig.colorbar(img, ax=ax, format="%+2.f dB")
plt.show()

# A spectrogram is a visual representation of the spectrum of frequencies of a signal as it varies with time. 
S = librosa.feature.melspectrogram(y=y,
								   sr=sr,
								   n_mels=128,
                                    fmax=8000)