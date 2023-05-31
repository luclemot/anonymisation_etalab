import pandas as pd
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests


def categorical_comparison(df, col1, col2):
    """Correlation study for categorical variables"""
    crosstab = pd.crosstab(df[col1], df[col2])
    chi2_score = chi2_contingency(crosstab)
    return (chi2_score[1], crosstab)


def p_vals_correction(pvals):
    """P-values correction"""
    rejected, p_adjusted, _, alpha_corrected = multipletests(
        pvals, alpha=0.05, method="bonferroni", is_sorted=False, returnsorted=False
    )
    sns.kdeplot(pvals, color="red", fill=True, label="raw")
    ax = sns.kdeplot(p_adjusted, color="green", shade=True, label="adjusted")
    ax.set(xlim=(0, 1))
    plt.title("distribution of p-values")
    plt.legend()


def numerical_correlation(df, num_cols):
    """Correlation study for numerical variables"""
    num_df = df[num_cols]
    corr = num_df.corr()
    sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)

    return None
