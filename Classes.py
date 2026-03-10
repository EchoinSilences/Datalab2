class Club():
    def __init__(self, team_id, team_name):
        self.team_id = team_id
        self.team_name = team_name
        
        self.matches = []
        self.players = []
        
    def add_player(self, player):
        self.players.append(player)
        
        
class Player():
    def __init__(self, id, name, height, weight, overall_rating, potential, preffered_foot, attacking_work_rate, defensive_work_rate, crossing, club_id):
        self.id = id
        self.name = name
        self.height = height
        self.weight = weight
        self.overall_rating = overall_rating
        self.potential = potential
        self.preffered_foot = preffered_foot
        self.attacking_work_rate = attacking_work_rate
        self.defensive_work_rate = defensive_work_rate
        self.crossing = crossing
        self.club_id = club_id