
import numpy as np
import pandas as pd

team_info = pd.read_csv("Team Info.csv")
# print(df.head())

#print(repr(team_info.columns.tolist()))

is_biased = True

def get_valid_team(team):
    if (team_info["Team Name"] == team).any():
        return team
    else:
        return "FCS"

def expected(team_A, team_B):
    return 1.0 / ( 1.0 + ( 7.5 ** ( ( team_B - team_A )/600 ) ) )

def report_game_result(home_team, away_team, home_points, away_points):

    #print(f"home: {home_team}")
    #print(get_valid_team(home_team))
    #print(f"away: {away_team}")
    #print(get_valid_team(away_team))

    # Actual results value
    if home_points > away_points:
        home_actual = 2 - (away_points / home_points)
        away_actual = away_points / home_points
    else:
        away_actual = 2 - (home_points / away_points)
        home_actual = home_points / away_points
    
    
    # Biased Score 
        
    home_b_score = team_info.loc[team_info["Team Name"] == home_team, "Current Biased Score"].iloc[0]
    away_b_score = team_info.loc[team_info["Team Name"] == away_team, "Current Biased Score"].iloc[0]
        # expected results
    home_b_expected = expected(home_b_score, away_b_score)
    away_b_expected = expected(away_b_score, home_b_score)
        # score adjustment
    home_b_adjustment = int(600 * (home_actual - home_b_expected))
    away_b_adjustment = int(600 * (away_actual - away_b_expected))

    
    # Unbiased Score 
        
    home_u_score = team_info.loc[team_info["Team Name"] == home_team, "Current Unbiased Score"].iloc[0]
    away_u_score = team_info.loc[team_info["Team Name"] == away_team, "Current Unbiased Score"].iloc[0]
        # expected results
    home_u_expected = expected(home_u_score, away_u_score)
    away_u_expected = expected(away_u_score, home_u_score)
        # score adjustment
    home_u_adjustment = int(600 * (home_actual - home_u_expected))
    away_u_adjustment = int(600 * (away_actual - away_u_expected))

    if home_team != "FCS":
        team_info.loc[team_info["Team Name"] == home_team, "Current Biased Score"] = home_b_score + home_b_adjustment

        team_info.loc[team_info["Team Name"] == home_team, "Current Unbiased Score"] = home_u_score + home_u_adjustment

    if away_team != "FCS":
        team_info.loc[team_info["Team Name"] == away_team, "Current Biased Score"] = away_b_score + away_b_adjustment
        
        team_info.loc[team_info["Team Name"] == away_team, "Current Unbiased Score"] = away_u_score + away_u_adjustment



    #print(f"Home B Adjustment: {home_b_adjustment}")
    #print(f"Away B Adjustment: {away_b_adjustment}")
    #print(f"Home U Adjustment: {home_u_adjustment}")
    #print(f"Away U Adjustment: {away_u_adjustment}")


def find_differing_team_names():
    games = pd.read_csv("GamesToAdd.csv")

    home_teams = games["Home Team"].to_list()
    away_teams = games["Away Team"].to_list()

    teams = home_teams + away_teams

    for t in team_info.iloc[:, 0]:
        if t in teams:
            teams = [x for x in teams if x != t]

    unique = list(set(teams))

    print("Not in team list")
    for i in unique:
        print(i)
    
#find_differing_team_names()

def adjust_for_games(games_to_add):
    games = pd.read_csv(games_to_add)

    for row in games.itertuples():
        report_game_result(get_valid_team(row.Home_Team), get_valid_team(row.Away_Team),
                           row.Home_Score, row.Away_Score)

    team_info.to_csv("Team Info.csv", index=False)

#report_game_result("Miami (FL)", "Duke", 0, 24)

adjust_for_games("GamesToAdd.csv")

def display_top_25():
    teams_sorted_u = team_info.sort_values(by= "Current Unbiased Score", ascending= False)
    print("Unbiased Top 25")
    for i in range(0, 25):
        print(f"{i+1}: {teams_sorted_u.iloc[i, 1]}")

    print("\n\n-----\n\n")
    
    teams_sorted_b = team_info.sort_values(by= "Current Biased Score", ascending= False)
    print("Biased Top 25")
    for j in range(0, 25):
        print(f"{j+1}: {teams_sorted_b.iloc[j, 1]}")

display_top_25()

def reset_current_score():
    team_info["Current Unbiased Score"] = team_info["Starting Unbiased Score"]
    team_info["Current Biased Score"] = team_info["Starting Biased Score"]
    team_info.to_csv("Team Info.csv", index=False)

#reset_current_score()

    



print("Done")