from driver import Driver

import sys, json, os

def main():
    game_id = sys.argv[1]
    os.makedirs(f"games/{game_id}", exist_ok=True)

    driver = Driver(game_id)
    summary_soup = driver.get_soup()
    boxscore_soup = driver.get_box_score()
    driver.close_driver()

    game_info = summary_soup.get_game_info()

    team_names = boxscore_soup.get_team_names()
    local_df, visitor_df = boxscore_soup.get_teams_df()

    local_df.drop_rows_any_na()
    visitor_df.drop_rows_any_na()
    
    local_df.save(f"games/{game_id}/{team_names[1]}.xlsx")
    visitor_df.save(f"games/{game_id}/{team_names[0]}.xlsx")
    
    game_summary = boxscore_soup.get_teams_stats()
    game_summary["Game Info"] = game_info
    with open(f"games/{game_id}/game_summary.json", "w") as json_file:
        json.dump(game_summary, json_file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()