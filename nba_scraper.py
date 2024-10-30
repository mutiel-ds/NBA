from scraper import Driver, Soup, Dataframe
import sys, json, os

if __name__ == "__main__":
    url = sys.argv[1]
    game_id = url.split("/")[4]
    os.makedirs(f"games/{game_id}", exist_ok=True)

    driver = Driver()
    soup = driver.get_url_soup(url)
    driver.close_driver()

    team_names = soup.get_team_names()
    local_df, visitor_df = soup.get_teams_df()
    
    local_df.save(f"games/{game_id}/{team_names[1]}.xlsx")
    visitor_df.save(f"games/{game_id}/{team_names[0]}.xlsx")
    
    game_summary = soup.get_game_summary()
    with open(f"games/{game_id}/game_summary.json", "w") as json_file:
        json.dump(game_summary, json_file, indent=4, ensure_ascii=False)