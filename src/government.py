# This file will be mostly about goverment *agents* more than the government as an institution. who's in goverment, opposition, legitimacy, and how they interact.
# This could end up being a huge but organized pile of classes for things like movements, parties, elections, and ministries.

# goverment, opposition, legitimacy, ministries/council politions, elections, political parties, political movements,  

class Government:
    def __init__(self, nation):
        self.nation = nation # reference to the nation which this government belongs
        self.legitimacy = 0 # 0-100
        self.ministries = [] # list of ministries or councils
        self.opposition = [] # list of opposition parties and/or interest groups
        self.political_parties = {} # dictionary of {party_name: [interest groups]}
        self.political_movements = [] # list of political movements active in the nation
        self.election = None # reference to the current, or previous election
        self.host_election() # check if an election is due and hold one if necessary
    
    def host_election(self):
        # Check if an election is due
        if self.election is None: #or self.election.date < date.today() - timedelta(years=4): #if no election or if the last election was more than 4 years ago
            # If an election is due, hold a new election
            self.election = Election()
            self.election.hold_election(self)
            return 

    def add_ministry(self, ministry):
        self.ministries.append(ministry)

    def remove_ministry(self, ministry):
        if ministry in self.ministries:
            self.ministries.remove(ministry)

    def add_opposition(self, opposition):
        self.opposition.append(opposition)

    def remove_opposition(self, opposition):
        if opposition in self.opposition:
            self.opposition.remove(opposition)

    def add_political_party(self, party):
        self.political_parties.append(party)

    def remove_political_party(self, party):
        if party in self.political_parties:
            self.political_parties.remove(party)

    def set_legitimacy(self):
        # Calculate legitimacy based on various factors
        # For now, just a placeholder
        self.legitimacy = 50

    def add_political_movement(self, movement):
        self.political_movements.append(movement)

    def remove_political_movement(self, movement):
        if movement in self.political_movements:
            self.political_movements.remove(movement)

class Election:
    def __init__(self):
        self.date = 0 # date of the election
        self.results = {} # dictionary to store election results
        self.polls = {} # dictionary of {party_name: projected votes}

    def hold_election(self, government):
        # Simulate an election
        campaining = True
        while campaining:
            self.polls = {} # dictionary of {party_name: sum of projected votes from member interest groups}
            for party, interest_groups in government.political_parties.items():
                total_votes = 0
                for group in interest_groups:
                    # Calculate votes based on group support and activism
                    total_votes = group.calculate_support() * group.calculate_activism()
                self.polls[party] = total_votes
        # after 6 months of campaigning, the election is held
        # Calculate the election results by solidifying the votes from the polls at the end of the campaign
        campaining = False
        election_results = {} # dictionary of {party_name: votes}
        for party, votes in self.polls.items():
            # Calculate the final votes based on the polls
            election_results[party] = votes
        return election_results


class PoliticalMovement:
    def __init__(self, name, ideology, attraction):
        self.name = name
        self.ideology = ideology 
        # support is percentage of population that supports this movement. 
        # (dont know yet if this will be the actual percent of the population or percent of total political power)
        self.support = 0 
        self.activism = 0 # level of activism (0-100) 
        self.attraction = attraction #dictionary of factors that attract people to this movement ex. {"pop trait": weight, "pop trait": weight}
        # might add an extra attribute for wether the movement is for secession or not 
        self.secession = False

    def calculate_support(self):
        # Calculate support based on attraction factors
        # For now, just a placeholder
        self.support = 50

    def calculate_activism(self):
        # Calculate activism based on various factors
        # For now, just a placeholder
        self.activism = 50

    def threaten_government(self):
        # Check if the movement is threatening the government, and actually do something about it
        # For now, just a placeholder
        return self.activism > 50