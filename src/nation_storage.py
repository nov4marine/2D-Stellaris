import json
import os

class NationStorage:
    FILE_PATH = "nations.json"

    @staticmethod
    def save_nation(nation):
        """Save a nation to the JSON file."""
        nations = NationStorage.load_nations()
        # Check if the nation already exists (by name)
        for existing_nation in nations:
            if existing_nation["name"] == nation.name:
                print(f"Nation '{nation.name}' already exists. Overwriting...")
                existing_nation.update(nation.to_dict())
                break
        else:
            nations.append(nation.to_dict())  # Add new nation if it doesn't exist
        with open(NationStorage.FILE_PATH, "w") as file:
            json.dump(nations, file, indent=4)

    @staticmethod
    def load_nations():
        """Load all nations from the JSON file."""
        if not os.path.exists(NationStorage.FILE_PATH):
            return []
        with open(NationStorage.FILE_PATH, "r") as file:
            return json.load(file)

    @staticmethod
    def delete_nation(nation_name):
        """Delete a nation by name."""
        nations = NationStorage.load_nations()
        nations = [nation for nation in nations if nation["name"] != nation_name]
        with open(NationStorage.FILE_PATH, "w") as file:
            json.dump(nations, file, indent=4)