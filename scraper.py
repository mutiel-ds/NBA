from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs

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


class Soup():
    def __init__(self, html):
        self.soup = bs(html, "lxml")

    def get_team_names(self):
        return [team.text for team in self.soup.find_all("h2")]
    
    def get_team_tables_soup(self):
        return self.soup.find_all("table")
    
    def get_table_columns(self, table):
        thead = table.find("thead")

        column_names = []
        for column in thead.find_all("th"):
            column_names.append(column.text)
        
        return column_names
    
    def get_table_players(self, table):
        table_columns = self.get_table_columns(table)
        
        tbody = table.find("tbody")
        players_rows = tbody.find_all("tr")[:-1]
        
        players_data = []
        for player in players_rows:
            
            player_info =  {}
            for idx, col in enumerate(player.find_all("td")):
                
                col_name = table_columns[idx]
                if idx == 0:
                    player_info[col_name] = col.find("span").find("span").text
                else:
                    player_info[col_name] = col.text
            
            players_data.append(player_info)

        return players_data

    def get_teams_df(self):
        team_tables = self.get_team_tables_soup()
        
        visitor_df = self._get_table_df(team_tables[0])
        local_df = self._get_table_df(team_tables[1])

        return local_df, visitor_df
    
    def _get_table_df(self, table):
        columns = self.get_table_columns(table)
        rows = self.get_table_players(table)
        return Dataframe(rows, columns)
    
    def get_teams_totals(self):
        team_tables = self.get_team_tables_soup()

        visitor_totals = self._get_table_totals(team_tables[0])
        local_totals = self._get_table_totals(team_tables[1])

        return local_totals, visitor_totals
    
    def _get_table_totals(self, table):
        table_columns = self.get_table_columns(table)

        tbody = table.find("tbody")
        players_rows = tbody.find_all("tr")[-1]

        totals = {}
        for idx, col in enumerate(players_rows):
            col_name = table_columns[idx]
            if idx != 1:
                totals[col_name] = col.text
            else:
                totals[col_name] = "240"

        return totals
    
    def get_game_summary(self):
        team_names = self.get_team_names()
        local_totals, visitor_totals = self.get_teams_totals()

        game_summary = {}
        game_summary["Local"] = {
            "Name": team_names[1],
            "Team Stats": local_totals
        }
        game_summary["Visitor"] = {
            "Name": team_names[0],
            "Team Stats": visitor_totals
        }

        return game_summary
    

class Driver():
    def __init__(self, show=True):
        self.show = show
        self.driver = self.init_driver()

    def init_driver(self):
        if self.show:
            driver = Firefox()
        else:
            options = Options()
            options.add_argument("--headless")
            driver = Firefox(options=options)

        return driver
    
    def close_driver(self):
        self.driver.close()
    
    def get_url_soup(self, url):
        self.driver.get(url)
        soup = Soup(self.driver.page_source)
        return soup