
from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Merchant(Context, event.Event):
    '''Encounter with a trading merchant. Uses the parser to decide what to do about it.'''
    def __init__(self):
        super().__init__()
        self.name = "merchant"
        self.pirates = []
        self.goods = ["medicine", "food", "firearm", "cutlass"]
        self.result = {}
        self.go = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "trade":
            if self.pirates:
                pirate = random.choice(self.pirates)
                item = random.choice(self.goods)
                self.result["message"] = f"The merchant trades {item} with {pirate}."
                self.pirates.remove(pirate)
            else:
                self.result["message"] = "The pirates have nothing to trade."
            self.go = True

        elif verb == "send off":
            self.result["message"] = "The merchant sails away, disappointed."
            self.go = True

        elif verb == "loot":
            if self.pirates:
                pirate = random.choice(self.pirates)
                loot = random.randint(50, 200)  # Random loot amount
                pirate.add_loot(loot)
                self.result["message"] = f"{pirate.get_name()} loots {loot} gold from the merchant!"
                self.pirates.remove(pirate)
            else:
                self.result["message"] = "The merchant has nothing left to loot."
            self.go = True

        else:
            self.result["message"] = "You can 'trade', 'send off', or 'loot' the merchant."
            self.go = False

    def process(self, world):
        self.go = False
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = "A merchant ship approaches. What do you want to do?"

        while not self.go:
            print(self.result["message"])
            action = input("Enter your action: ").strip().lower()
            self.process_verb(action, [], [])
            world.resolve_effects(self.result)

        return self.result
