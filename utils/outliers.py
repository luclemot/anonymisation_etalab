from utils.tools import col_set
from sklearn import preprocessing
from kmodes.kmodes import KModes
from kmodes.kprototypes import KPrototypes
from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def identify_outliers(df, target, cat_cols, n):
    """Identifies outliers for all combinations of categorical variables.
    Datapoints are considered outliers if there are less than n with the same attributes.
    """
    dic = {}
    set_cols = col_set(cat_cols)
    set_cols.remove([])
    for i, combin in enumerate(set_cols):
        grouped_df = df.groupby(combin, as_index=False)[target].count()
        outliers = grouped_df.loc[grouped_df[target] < n]
        if (not outliers.empty) and (tuple(combin) not in list(dic.keys())):
            dic[tuple(combin)] = outliers
    return dic


def explore_outliers(df, col_combine):
    """Shows the datapoints with the col_combine attributes from the df dataframe."""
    res = df.copy()
    for x, y in col_combine.items():
        res = res.loc[res[x] == y]
    return res


def identify_num_outliers(df, num_cols, target):
    """Plots a scatter matrix on numerical variables, with target color."""
    fig = px.scatter_matrix(df, dimensions=num_cols, color=target)
    fig.show()


def cluster(df, n_clusters, num_cols=None, cat_cols=None):
    """Creates a clusterization and plots the distribution based on n_clusters,
    and catgegorical and numerical column names."""
    temp_norm = df.copy()
    kcluster = None

    if num_cols:
        scaler = preprocessing.MinMaxScaler()
        temp_norm[num_cols] = scaler.fit_transform(temp_norm[num_cols])
        if not cat_cols:
            kcluster = KMeans(n_clusters=n_clusters)
            clusters = kcluster.fit_predict(temp_norm)

    if cat_cols is not None:
        columns = df.columns
        cat_cols = [columns.get_loc(column_name) for column_name in cat_cols]
        if not num_cols:
            kcluster = KModes(n_clusters=n_clusters)
            clusters = kcluster.fit_predict(temp_norm)

    if kcluster is None:
        kcluster = KPrototypes(n_clusters=100, init="Cao")
        clusters = kcluster.fit_predict(temp_norm, categorical=cat_cols)

    labels = pd.DataFrame(clusters)
    labeled = pd.concat((df, labels), axis=1)
    labeled = labeled.rename({0: "labels"}, axis=1)

    labeled["Constant"] = 0  # dummy feature for plotting

    size = len(df.columns)
    # f, axes = plt.subplots(1, size, figsize=(25, 7), sharex=False)
    # f.subplots_adjust(hspace=0.2, wspace=0.7)

    for i in range(size):
        col = labeled.columns[i]
        if i in cat_cols:
            sns.catplot(x=col, y="labels", kind="swarm", hue="labels", data=labeled)
        else:
            sns.swarmplot(
                x=labeled["Constant"], y=labeled[col].values, hue=labeled["labels"]
            )

    plt.close(2)
    plt.close(3)
    plt.show()
