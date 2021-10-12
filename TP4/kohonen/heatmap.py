import numpy as np
from matplotlib import pyplot as plt

"""
CÓDIGO SACADO DEL LINK: 
    https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
Adaptado a nuestro TP. No está idéntico al código del link

Otro link interesante (no lo usamos):
    https://plotly.com/python/heatmaps/
"""


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, pixel_text_map: dict, data=None,
                     textcolors=("black", "white"), threshold=None, **textkw):
    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text_to_write = ""
            array_of_country_names = pixel_text_map.get((i, j))
            for name in array_of_country_names:
                text_to_write += name + ",\n"
            text = im.axes.text(j, i, text_to_write, **kw)
            texts.append(text)
    return texts


def plot_matrix(matrix, text_map):
    row_labels = ["" for _ in range(matrix.shape[0])]
    col_labels = ["" for _ in range(matrix.shape[0])]

    fig, ax = plt.subplots()
    im, cbar = heatmap(matrix, row_labels, col_labels, ax=ax, cmap="YlGn", cbarlabel="# of cities")
    texts = annotate_heatmap(im, pixel_text_map=text_map)

    fig.tight_layout()
    plt.show()


def plot_matrix_u(matrix_u):
    row_labels = ["" for _ in range(matrix_u.shape[0])]
    col_labels = ["" for _ in range(matrix_u.shape[0])]

    fig, ax = plt.subplots()
    im = ax.imshow(matrix_u)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(row_labels)))
    ax.set_yticks(np.arange(len(col_labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(row_labels)
    ax.set_yticklabels(col_labels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(matrix_u.shape[0]):
        for j in range(matrix_u.shape[1]):
            text = ax.text(j, i, round(matrix_u[i, j], 2), ha="center", va="center", color="w")

    ax.set_title("Matrix U")
    fig.tight_layout()
    plt.show()
