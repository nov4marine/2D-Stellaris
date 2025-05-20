
class InterestGroup:
    def __init__(self, name, description, nation, ideologies=None):
        """the interest group class, which is a collection of ideologies and members"""
        self.name = name
        self.description = description
        self.nation = nation

        self.ideologies = []
        self.clout = 0
        self.members = [] # List of members in the interest group across the nation
        self.approval = 0 # Approval rating of the interest group with the government. probably between -100 and 100

    def add_ideology(self, ideology):
        """Add an ideology to the interest group."""
        if ideology not in self.ideologies:
            self.ideologies.append(ideology)
            print(f"{ideology} added to {self.name} interest group.")
        else:
            print(f"{ideology} is already in {self.name} interest group.")

    def remove_ideology(self, ideology):
        """Remove an ideology from the interest group."""
        if ideology in self.ideologies:
            self.ideologies.remove(ideology)
            print(f"{ideology} removed from {self.name} interest group.")
        else:
            print(f"{ideology} is not in {self.name} interest group.")

    def calculate_clout(self):
        """Calculate the clout of the interest group based on its members."""
        self.clout = sum(pop.political_power for member in self.members) # times the sum of modifiers
        print(f"{self.name} interest group clout calculated: {self.clout}")

class Ideology:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.stances = {} # Dictionary to hold stances on various issues

    def get_stance(self, issue):
        """Get the stance of the ideology on a specific issue."""
        return self.stances.get(issue, "Neutral")
    
transhumanism = Ideology("Transhumanism", "The belief in the enhancement of the human condition through advanced technology.")
transhumanism.stances = {
    "genetic_modification": "Support",
    "cybernetic_enhancement": "Support",
    "artificial_intelligence": "Support",
    "climate_change": "Neutral",
    "space_exploration": "Support"
}

techno_authoritarianism = Ideology("Techno-Authoritarianism", "A political ideology that advocates for a strong, centralized government that uses technology to maintain control and order.")
techno_authoritarianism.stances = {
    "genetic_modification": "Support",
    "cybernetic_enhancement": "Support",
    "artificial_intelligence": "Support",
    "climate_change": "Neutral",
    "space_exploration": "Support"
}

cosmopolitanism = Ideology("Cosmopolitanism", "The ideology that all species belong to a single community, based on a shared morality.")
cosmopolitanism.stances = {
    "distribution of Power": "Universal Suffrage",
    "Ai Rights": "Support",
    "military Expansion": "Neutral"
}

jingoism = Ideology("Jingoism", "An extreme form of nationalism characterized by aggressive foreign policy and military expansion.")
jingoism.stances = {
    "distribution of Power": "Universal Suffrage",
    "Ai Rights": "Oppose",
    "military Expansion": "Support"
}

cyber_syndicalism = Ideology("Cyber-Syndicalism", "A political ideology that advocates for the use of technology to empower workers and promote social justice.")
cyber_syndicalism.stances = {
    "distribution of Power": "Universal Suffrage",
    "Ai Rights": "Support",
    "military Expansion": "Neutral"
}

megacorporatism = Ideology("Megacorporatism", "A political ideology that advocates for the dominance of large corporations in society and the economy.")
megacorporatism.stances = {
    "distribution of Power": "Universal Suffrage",
    "Ai Rights": "Oppose",
    "military Expansion": "Neutral"
}

bio_conservatism = Ideology("Bio-Conservatism", "A political ideology that advocates for the preservation of traditional human values and ethics in the face of technological advancement.")
bio_conservatism.stances = {
    "genetic_modification": "Oppose",
    "cybernetic_enhancement": "Oppose",
    "artificial_intelligence": "Oppose",
    "climate_change": "Neutral",
    "space_exploration": "Neutral"
}

psionicism = Ideology("Psionicism", "A political ideology that advocates for the exploration and development of psionic abilities and technologies.")
psionicism.stances = {
    "genetic_modification": "Support",
    "cybernetic_enhancement": "Support",
    "artificial_intelligence": "Support",
    "climate_change": "Neutral",
    "space_exploration": "Support"
}

eugenicism = Ideology("Eugenicism", "A political ideology that advocates for the improvement of the human population through selective breeding and genetic engineering.")
eugenicism.stances = {
    "genetic_modification": "Support",
    "cybernetic_enhancement": "Support",
    "artificial_intelligence": "Support",
    "climate_change": "Neutral",
    "space_exploration": "Support"
}

