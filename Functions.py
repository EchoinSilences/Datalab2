from Classes import *

def Load_players(club, player_df, player_attribute_df, player_ids):
    for p_id in player_ids:
        player = player_df[player_df['player_api_id'] == p_id]
        player_attributes = player_attribute_df[player_attribute_df['player_api_id'] == p_id]
        
        id = p_id
        name = player['player_name']
        height = player['height']
        weight = player['weight']
        overall_rating = player_attributes['overall_rating']
        potential = player_attributes['potential']
        preffered_foot = player_attributes['preferred_foot']
        attacking_work_rate = player_attributes['attacking_work_rate']
        defensive_work_rate = player_attributes['defensive_work_rate']
        crossing = player_attributes['crossing']
        club_id = club.team_id
        
        club.add_player(Player(id, name, height, weight, overall_rating, potential, preffered_foot, attacking_work_rate, defensive_work_rate, crossing, club_id))