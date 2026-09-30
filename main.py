
import numpy as np
import pandas as pd

team_info = pd.read_csv("Team Info.csv")
# print(df.head())

#print(repr(team_info.columns.tolist()))

is_biased = True

def expected(team_A, team_B):
    return 1.0 / ( 1.0 + ( 7.5 ** ( ( team_B - team_A )/600 ) ) )

def report_game_result(home_team, away_team, home_points, away_points):

    # Actual results value
    if home_points > away_points:
        home_actual = 1 - (away_points / home_points)
        away_actual = away_points / home_points
    else:
        away_actual = 1 - (home_points / away_points)
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

    #print(f"Home B Adjustment: {home_b_adjustment}")
    #print(f"Away B Adjustment: {away_b_adjustment}")
    #print(f"Home U Adjustment: {home_u_adjustment}")
    #print(f"Away U Adjustment: {away_u_adjustment}")

    

report_game_result("Miami (FL)", "Duke", 0, 24)

    



print("Done")