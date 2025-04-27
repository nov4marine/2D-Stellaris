class Action:
    def __init__(self, executor=None):
        """Base class for actions taken by a given executor. Executor can be player or AI."""
        self.executor = executor

    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")

class ManageEconomyAction(Action):
    def __init__(self, nation):
        super().__init__(executor=nation)

    def execute(self):
        self.executor['gdp'] += 1000
        print(f"{self.executor['name']}'s GDP is now {self.executor['gdp']}")

class ActionManager:
    def execute_action(self, action):
        action.execute()

################################################

class GenericAction(Action):
    def __init__(self, executor, action_type, parameters=None):
        super().__init__(executor)
        self.action_type = action_type
        self.parameters = parameters

    def execute(self):
        if self.action_type == "manage_economy":
            self.executor.gdp += self.parameters.get("amount", 1000)
            print(f"{self.executor.name}'s GDP increased to {self.executor.gdp}")
        elif self.action_type == "build_ship":
            print(f"{self.executor.name} is building {self.parameters['ship_type']}!")
            