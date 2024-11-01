from bs4 import BeautifulSoup as bs
from dataframe import Dataframe

class Soup():
    def __init__(self, html):
        self.soup = bs(html, "lxml")

    def get_game_info(self):
        """
        Function to retrieve game info from summary page
        """
        info_card = self.soup.find_all("div", {"class": "InfoCard_column__et46d"})
        game_info = {}
        for info_idx in range(len(info_card)//2):
            info_key = info_card[info_idx*2].text
            info_value = info_card[info_idx*2+1]
            if info_key not in game_info:
                if info_value.find("a"):
                    game_info[info_key] = str(info_value.find("a").get("href"))
                else:
                    game_info[info_key] = str(info_value.text)
        return game_info

    def get_team_names(self):
        """
        Function to get the teams that played that game from box score page
        """
        return [team.text for team in self.soup.find_all("h2")]
    
    def get_team_tables_soup(self):
        """
        Function to get the team tables where the player stats are stored
        """
        return self.soup.find_all("table")
    
    def get_table_columns(self, table):
        """
        Function to get the table column names of the team tables
        """
        thead = table.find("thead")

        column_names = []
        for column in thead.find_all("th"):
            column_names.append(column.text)
        
        return column_names
    
    def get_table_players(self, table):
        """
        Function to get the player stats from the team table
        """
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
        """
        Function to get a Dataframe object for each team's players stats
        """
        team_tables = self.get_team_tables_soup()
        
        visitor_df = self._get_table_df(team_tables[0])
        local_df = self._get_table_df(team_tables[1])

        return local_df, visitor_df
    
    def _get_table_df(self, table):
        """
        Function to initiate the Dataframe object with the table elements
        """
        columns = self.get_table_columns(table)
        rows = self.get_table_players(table)
        return Dataframe(rows, columns)
    
    def get_teams_totals(self):
        """
        Function to get the teams' final stats
        """
        team_tables = self.get_team_tables_soup()

        visitor_totals = self._get_table_totals(team_tables[0])
        local_totals = self._get_table_totals(team_tables[1])

        return local_totals, visitor_totals
    
    def _get_table_totals(self, table):
        """
        Function to get an specific team's total stats
        """
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
    
    def get_teams_stats(self):
        """
        Function to generate the game summary containing the game info and both teams' final stats
        """
        team_names = self.get_team_names()
        local_totals, visitor_totals = self.get_teams_totals()

        teams_stats = {}
        teams_stats["Local"] = {
            "Name": team_names[1],
            "Team Stats": local_totals
        }
        teams_stats["Visitor"] = {
            "Name": team_names[0],
            "Team Stats": visitor_totals
        }

        return teams_stats
