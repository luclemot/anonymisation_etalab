import datetime

import numpy as np
import pandas as pd
import random

from pandas.api.types import is_float_dtype, is_integer_dtype

from cape_dataframes.pandas import dtypes
from cape_dataframes.pandas.transformations import DatePerturbation
from cape_dataframes.pandas.transformations import NumericPerturbation


def numerical_perturbation(df, num_cols):
    for col in num_cols:
        min = df[col].min()
        max = df[col].max()
        if is_float_dtype(df[col].dtype):
            print("float")
            noise = np.random.random(size=len(df[col])) * (max - min)
            # transform = NumericPerturbation(dtype=dtypes.Float, min=-5, max=5)
        elif is_integer_dtype(df[col].dtype):
            print("int")
            noise = np.random.randint(-5, 5, size=len(df[col]))
            transform = NumericPerturbation(dtype=dtypes.Integer, min=-5, max=5)
        # df[col] = transform(df[col])
        df[col] = df[col] + noise
    return df


def datetime_perturbation(df, dat_cols):
    # transform = DatePerturbation(frequency="DAY", min=-10, max=10, seed=1234)
    # transform = DatePerturbation(frequency=("DAY", "YEAR"), min=(-10, -5), max=(10, 5), seed=1234)
    pass


if __name__ == "__main__":
    df = pd.DataFrame([0, 1, 0, 1, 2], ["a", "b", "c", "d", "e"])
    df.rename(columns={0: "number", 1: "letter"}, inplace=True)
    print(df)
    numerical_perturbation(df, ["number"])
    print(df)
