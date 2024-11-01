import pandas as pd

class Dataframe():
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.df = self.init_df()

    def init_df(self):
        return pd.DataFrame(data=self.rows, columns=self.columns)
    
    def drop_rows_any_na(self):
        self._dropna(axis="index", how="any")

    def drop_cols_any_na(self):
        self._dropna(axis="columns", how="any")

    def drop_rows_all_na(self):
        self._dropna(axis="index", how="all")

    def drop_cols_all_na(self):
        self.dropna(axis="columns", how="all")

    def _dropna(self, axis, how):
        self.df.dropna(axis=axis, how=how, inplace=True)

    def save(self, path):
        self.df.to_excel(path, index=False)