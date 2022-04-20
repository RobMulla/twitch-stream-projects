import matplotlib.pylab as plt
import numpy as np

def load_combine_canvas(row):
    imgc0 = plt.imread(row[0])
    if type(row[1]) == str:
        imgc1 = plt.imread(row[1])
    else:
        imgc1 = np.zeros_like(imgc0)

    if type(row[2]) == str:
        imgc2 = plt.imread(row[2])
    else:
        imgc2 = np.zeros_like(imgc0)

    if type(row[3]) == str:
        imgc3 = plt.imread(row[3])
    else:
        imgc3 = np.zeros_like(imgc0)

    img_combined = np.concatenate(
        [
            np.concatenate([imgc0, imgc1], axis=1),
            np.concatenate([imgc2, imgc3], axis=1),
        ],
        axis=0,
    )
    return img_combined

def unstack_metadata(meta_data):
    # Metadata when there are 4 canvas
    four_views = meta_data.groupby(["dt", "canvas"])["filename_full"].first().unstack()
    return four_views