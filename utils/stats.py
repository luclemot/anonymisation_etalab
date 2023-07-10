import pandas as pd
import matplotlib.pyplot as plt


def info_loss(original_df, anonym_df, cat_cols):
    """Interprets the loss information in terms of categorical column values and total row count."""
    for col in cat_cols:
        loss = anonym_df[col].nunique() / original_df[col].nunique()
        print(
            "On conserve {:.2f}% de valeurs présentes dans la colonne {}.".format(
                loss * 100, col
            )
        )
    print(
        "On conserve {:.2f}% des lignes présentes dans le tableau initial.".format(
            (len(anonym_df) / len(original_df)) * 100
        )
    )


def plot_info_loss(original_df, anonym_df, cat_cols):
    res = pd.DataFrame(
        columns=["Variable", "Number of values / Former number of values"]
    )
    for col in cat_cols:
        loss = anonym_df[col].nunique() / original_df[col].nunique()
        res.loc[len(res)] = [col, loss]
    res.plot.bar(
        x="Variable",
        y="Number of values / Former number of values",
        color="lightseagreen",
        width=0.6,
        figsize=(7, 5),
    )
    plt.axhline(y=1, color="tomato", linestyle="dashed")
    plt.show()


def categorical_loss(original_df, anonym_df, cat_cols):
    # on va comparer les tables de contingence + les valeurs liées à l'entropie
    return None


def numerical_loss(original_df, anonym_df, num_cols):
    for col in num_cols:
        mean_evol = (original_df[col].mean() - anonym_df[col].mean()) / original_df[
            col
        ].mean()
        print(
            "For the column {}, the mean value changed by {}%".format(
                col, mean_evol * 100
            )
        )
        # Doesn't mean anything since we scaled the anonymized value.
        std_evol = (original_df[col].std() - anonym_df[col].std()) / original_df[
            col
        ].std()
        print(
            "For the column {}, the std value changed by {}%".format(
                col, std_evol * 100
            )
        )

        corr = original_df[col].corr(anonym_df[col])
        print(
            "The correlation between the original and anonymized data on column {} is {}%".format(
                col, corr * 100
            )
        )

    # compute correlation post PCA ?
