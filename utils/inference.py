from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np


class Infer_Model:
    def __init__(self, df, cat_cols, num_cols, target):
        self.df = df.copy()
        self.cat_cols = cat_cols
        self.num_cols = num_cols
        self.target = target
        self.target_type = self.df[target].dtype

    def prep_data(self):
        # On veut tokenizer les variables dans cat_cols, scaler les variables dans num_cols, et créer le train, test split en fonction
        for col in self.num_cols:
            scaler = StandardScaler()
            # Why not MinMaxScaler?
            self.df[col] = scaler.fit_transform(np.array(self.df[col]).reshape(-1, 1))
        for col in self.cat_cols:
            if col != self.target:
                # LabelEncoder ?
                # voc = Vocabulary(col)
                # voc.load_words(content=self.df[col])
                # self.df[col] = [voc.tokenize(t) for t in self.df[col]]
                # initialize
                cv = CountVectorizer(token_pattern=r"(?u)\b\w+\b")
                cv_matrix = cv.fit_transform(self.df[col])
                # create document term matrix
                df_dtm = pd.DataFrame(
                    cv_matrix.toarray(),
                    index=self.df.index,
                    columns=cv.get_feature_names_out(),
                )
                # on veut drop celles en commun
                self.df = pd.merge(
                    self.df,
                    df_dtm,
                    left_index=True,
                    right_index=True,
                    suffixes=["", "_y"],
                )
                self.df = self.df[[c for c in self.df.columns if not c.endswith("_y")]]
                try:
                    self.df.drop(columns=[col, "ou"], inplace=True)
                except:
                    self.df.drop(columns=[col], inplace=True)

    def split(self):
        cols = list(self.df.columns)
        cols.remove(self.target)
        x_train, x_test, y_train, y_test = train_test_split(
            self.df[cols],
            self.df[self.target],
            test_size=0.2,
        )
        return (x_train, x_test, y_train, y_test)

    def classifier(self):
        # si target est catégorielle, entrainer, save le modèle
        clf = RandomForestClassifier()
        return clf

    def regressor(self):
        # reg = LinearRegression()
        reg = GradientBoostingRegressor()
        return reg

    def train_model(self, x_train, x_test, y_train, y_test):
        # prep_data(self)
        if self.target_type == float or self.target_type == int:
            model = self.regressor()
            model.fit(x_train, y_train)
        else:
            model = self.classifier()
            model.fit(x_train, y_train)
            # pred = clf.predict(x_test)
        # on calcule une métrique de performance, on rend la métrique + le modèle (à tester pour l'utilisateur)
        return model


class Vocabulary:
    def __init__(self, name):
        UNK_token = 0  # Used for unkown values

        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {UNK_token: "UNK"}
        self.num_words = 1

    def add_word(self, word):
        if word not in self.word2index:
            # First entry of word into vocabulary
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            # Word exists; increase word count
            self.word2count[word] += 1

    def load_words(self, content):
        for i, line in enumerate(content):
            for word in line.split():
                self.add_word(word)

    def tokenize(self, sentence):
        return [self.word2index[word] for word in sentence.split()]

    def to_word(self, index):
        return self.index2word[index]

    def to_index(self, word):
        return self.word2index[word]


def compare_models(
    model, original_model, validation_set_X, validation_set_y, print_bool: bool
):
    model_score = model.score(validation_set_X, validation_set_y)
    original_score = original_model.score(validation_set_X, validation_set_y)
    if print_bool:
        print("A model trained on the original data has the following accuracy : ")
        print(original_score)
        print("A model trained on the anonymized data has the following accuracy : ")
        print(model_score)
        print("The change in performance is of (%) :")
        print((original_score - model_score) * 100)
    return original_score * 100, model_score * 100, (original_score - model_score) * 100
