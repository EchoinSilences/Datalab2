import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

class Club():
    """
        Description: 
            Deze class representeert een voetbalclub. Het bevat informatie over de club en DataFrames voor spelers en wedstrijden.
        
        Attributes:
            team_id: id van de club.
            team_name: De naam van de club.
            matches_df: DataFrame met wedstrijden van de club.
            players_df: DataFrame met spelers van de club.
            
         Methods:
            load_players(player_df, player_attribute_df, player_ids): 
                Laadt spelers in de club als DataFrame op basis van player_ids.
            load_matches(matches_df): 
                Laadt wedstrijden van de club als DataFrame.
            get_season_matches(season): 
                Haalt wedstrijden van een bepaald seizoen.
            calculate_stats(): 
                Berekent statistieken voor het team.
    """
    
    def __init__(self, team_id, team_name):
        """
            Description:
                De constructor van de Club class.
                
            Args:
                self: Het club object.
                team_id: id van de club.
                team_name: De naam van de club.
                
            Returns:
                None
            
        """
        self.team_id = team_id
        self.team_name = team_name
        
        self.matches_df = pd.DataFrame()
        self.players_df = pd.DataFrame()
        
        
        
    def load_players(self, player_df, player_attribute_df, player_ids):
        """
            Description:
                Laadt spelers in de club op basis van player_ids als DataFrame.
                
            Args:
                self: Het club object.
                player_df: Een dataframe met informatie over de spelers.
                player_attribute_df: Een dataframe met informatie over de attributen van de spelers.
                player_ids: Een lijst van player_ids die bij de club horen.
                
            Returns:
                None
        """
        # Filter DataFrames voor deze club
        filtered_players = player_df[player_df['player_api_id'].isin(player_ids)].copy()
        filtered_attributes = player_attribute_df[player_attribute_df['player_api_id'].isin(player_ids)].copy()
        
        # Merge player info met attributes
        merged = filtered_players.merge(filtered_attributes, on='player_api_id', how='left')
        
        # Voeg toe aan club DataFrame
        self.players_df = pd.concat([self.players_df, merged], ignore_index=True)
        
    def load_matches(self, matches_df):
        """
            Description:
                Laadt alle wedstrijden van deze club uit een matches DataFrame.
                
            Args:
                self: Het club object.
                matches_df: Een DataFrame met alle wedstrijden.
                
            Returns:
                None
        """
        # Filter naar wedstrijden waar deze club home of away team is
        club_matches = matches_df[(matches_df['home_team_api_id'] == self.team_id) | (matches_df['away_team_api_id'] == self.team_id)].copy()
        
        self.matches_df = club_matches
        
    def get_season_matches(self, season):
        """
            Description:
                Haalt alle wedstrijden van een bepaald seizoen.
                
            Args:
                self: Het club object.
                season: Het seizoen (bijv. '2015/2016').
                
            Returns:
                DataFrame met wedstrijden van dat seizoen.
        """
        return self.matches_df[self.matches_df['season'] == season]
    
    def calculate_stats(self, season=None):
        """
            Description:
                Berekent statistieken voor het team in een bepaald seizoen.
                
            Args:
                self: Het club object.
                season: Het seizoen (optioneel). Als None, alle seizoenen.
                
            Returns:
                Dictionary met statistieken.
        """
        if season:
            matches = self.get_season_matches(season)
        else:
            matches = self.matches_df
        
        if len(matches) == 0:
            return {}
        
        # Bereken wins, draws, losses
        wins = len(matches[
            ((matches['home_team_api_id'] == self.team_id) & (matches['home_team_goal'] > matches['away_team_goal'])) |
            ((matches['away_team_api_id'] == self.team_id) & (matches['away_team_goal'] > matches['home_team_goal']))
        ])
        
        draws = len(matches[matches['home_team_goal'] == matches['away_team_goal']])
        losses = len(matches) - wins - draws
        
        goals_for = matches[matches['home_team_api_id'] == self.team_id]['home_team_goal'].sum() + \
                    matches[matches['away_team_api_id'] == self.team_id]['away_team_goal'].sum()
        
        goals_against = matches[matches['home_team_api_id'] == self.team_id]['away_team_goal'].sum() + \
                        matches[matches['away_team_api_id'] == self.team_id]['home_team_goal'].sum()
        
        points = (wins * 3) + (draws * 1)
        
        return {
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goals_for - goals_against,
            'points': points,
            'matches_played': len(matches)
        }
       
class Player():
    """Simple player class (optional, kept for reference)"""
    def __init__(self, id, name, height, weight, overall_rating, potential, preffered_foot):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.overall_rating = overall_rating
        self.potential = potential
        self.preffered_foot = preffered_foot
        
class Match():
    """Simple match class (optional, kept for reference)"""
    def __init__(self, match_id, home_team_api_id, away_team_api_id, home_team_goal, away_team_goal):
        self.match_id = match_id
        self.home_team_api_id = home_team_api_id
        self.away_team_api_id = away_team_api_id
        self.home_team_goal = home_team_goal
        self.away_team_goal = away_team_goal
        
class Research():
    """
        Description:
            Deze class bevat methoden voor het uitvoeren van onderzoek en analyses op de club data.
            
        Attributes:
            Data    
        
        Methods:
            correlation_analysis(club): 
                Voert een correlatieanalyse uit op de performance van het team in een seizoen.
                
            player_analysis(club): 
                Voert een analyse uit op de spelers van het team, zoals gemiddelde ratings en attributen.
                
            match_analysis(club):
                Voert een analyse uit op de wedstrijden van het team, zoals doelpunten per wedstrijd en resultaten.      
    """
    
    def init(self, data):
        self.data = data
          
    def correlation_analysis(self, club, season):
        """
            Description:
                Voert een correlatieanalyse uit op de performance van het team in een seizoen.
                
            Args:
                self: Het Research object.
                club: Het Club object.
                season: Het seizoen om te analyseren (bijv. '2015/2016').
                
            Returns:
                Correlatiematrix als DataFrame.
        """
        season_matches = club.get_season_matches(season)
        
        if season_matches.empty:
            print(f'Geen matches gevonden voor {club.team_name} in season {season}.')
            return pd.DataFrame()
        
        # Selecteer relevante kolommen voor correlatieanalyse
        relevant_columns = ['home_team_goal', 'away_team_goal', 'home_team_shots', 'away_team_shots', 'home_team_possession', 'away_team_possession']
        correlation_data = season_matches[relevant_columns]
        correlation_matrix = correlation_data.corr().sort_values(ascending=False)
        
        return correlation_matrix
    
    def player_analysis(self, club):
        """
            Description:
                Voert een analyse uit op de spelers van het team, zoals gemiddelde ratings en attributen.
                
            Args:
                self: Het Research object.
                club: Het Club object.
                
            Returns:
                DataFrame met gemiddelde ratings en attributen van spelers.
        """
        if club.players_df.empty:
            print(f'Geen spelers gevonden voor {club.team_name}.')
            return pd.DataFrame()
        
        # Bereken gemiddelde ratings en attributen
        player_avg_stats = club.players_df.groupby('player_api_id').agg({
            'overall_rating': 'mean',
            'potential': 'mean',
            'height': 'mean',
            'weight': 'mean'
        }).reset_index()
        
        return player_avg_stats
    
    def match_analysis(self, club):
        """
            Description:
                Voert een analyse uit op de wedstrijden van het team, zoals doelpunten per wedstrijd en resultaten.
                
            Args:
                self: Het Research object.
                club: Het Club object.
                
            Returns:
                DataFrame met analyse van wedstrijden, zoals doelpunten per wedstrijd en resultaten.
        """
        
        if club.matches_df.empty:
            print(f'Geen matches gevonden voor {club.team_name}.')
            return pd.DataFrame()
        
        # Bereken doelpunten per wedstrijd en resultaten
        club.matches_df['total_goals'] = club.matches_df['home_team_goal'] + club.matches_df['away_team_goal']
        club.matches_df['result'] = np.where(
                                        (club.matches_df['home_team_api_id'] == club.team_id) & 
                                        (club.matches_df['home_team_goal'] > club.matches_df['away_team_goal']), 'win',
                                    np.where(
                                        (club.matches_df['away_team_api_id'] == club.team_id) & 
                                        (club.matches_df['away_team_goal'] > club.matches_df['home_team_goal']), 'win', 
                                    np.where(
                                        club.matches_df['home_team_goal'] == club.matches_df['away_team_goal'],  'draw',
                                                                                                                 'loss'
                                        )
                                    )
                                )
        
        return club.matches_df[['match_id', 'season', 'total_goals', 'result']]
        