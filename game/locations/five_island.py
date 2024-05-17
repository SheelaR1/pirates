from game import location
from game.display import announce
import game.config as config
from game.items  import Item
import game.items as items
from game.events import *

class five_island(location.Location):
    def __init__(self,x,y,w):
        super().__init__(x, y, w)
        self.name = "Five Island"
        self.symbol = "I"
        self.visitable = True
        self.starting_location = Beach(self)
        self.locations = {
            "beach": self.starting_location,
            "forest": Forest(self),
            "cave": Cave(self),
            "cliff": Cliff(self),
            "ruins": Ruins(self)
        }

    def enter(self, ship):
        announce("You've arrived at the Five Island.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()


class Beach(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"  
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self

        self.treasure_collected = False
        self.treasure = items.Treasure("Mystery Diamond", 100)

    def enter(self):
        announce(
            " Choose a location to visit: \nBeach \nForest  \nCave  \nCliff \nRuins \nLeave Island\n"
        )
        if self.treasure_collected== False:
            announce(
                "You step onto the sandy shores of the Five Beach, noticing something hidden in the sand."
            )
            self.treasure = items.Treasure("Unique Crystal", 50)
            self.treasure_collected = True
        else:
            announce("You walk along the familiar sandy shores of the Mystery Beach.")

        announce(
            "You are on the  Beach. Choose a location to explore: \nForest  \nCave  \nCliff \nRuins\n"
        )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False


class Forest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "forest"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self
        self.event_chance = 25

        self.riddle_solved = False
        self.treasures = [
            items.Treasure("Diamond", 100),
            items.Treasure("Crystal", 100),
        ]
        self.treasures_collected = False

    def enter(self):
        if not self.treasures_collected and not self.riddle_solved:
            announce(
                "You venture into the dense, mysterious forest, sensing hidden treasures and a challenge awaiting."
            )
            self.collect_treasures()
            self.treasures_collected = True
            self.start_encounter()
        elif not self.riddle_solved:
            announce(
                "The dense forest seems less mysterious now, but the challenge still awaits with its unsolved riddle."
            )
            self.start_encounter()
        else:
            announce(
                "The forest is peaceful, and the challenge now a memory."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb in self.main_location.locations:
            config.the_player.next_loc = self.main_location.locations[verb]
        elif verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        

    def collect_treasures(self):
        for treasure in self.treasures:
            announce(f"You found a {treasure.name} worth {treasure.value} points!")
            config.the_player.add_to_inventory(treasure)
        announce("You have collected all the scattered treasures in the forest!")

    def start_encounter(self):
        announce(
            "A voice echoes from the depths of the forest: 'Solve my riddle to pass: What has keys but cannot open doors ?"
        )
        self.solve_riddle()

    def solve_riddle(self):
        player_answer = input("Your answer: ").strip().lower()
        if player_answer == "piano":
            announce("Correct! You may pass.")
            self.riddle_solved = True
        else:
            announce("Incorrect! Try again.")
            self.start_encounter()



class Cliff(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cliff"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self

        self.event_chance = 20
        self.treasure = items.Treasure("Ancient Coin", 200)
        self.treasure_collected = False

    def enter(self):
        if not self.treasure_collected:
            announce(
                "You stand at the edge of a high cliff, a glint from the ground catching your eye."
            )
            self.treasure_collected = True
            announce(
                "You notice a zipline nearby. Would you like to zipline from the cliff? (yes/no)"
            )
            choice = input().strip().lower()
            if choice == "yes":
                announce(
                    "You take the zipline and experience a thrilling adventure!"
                )
            elif choice == "no":
                announce(
                    "You decide to enjoy the view from the cliff."
                )
        else:
            announce(
                "The cliff offers a breathtaking view of the sea, the mystery of the hidden treasure now solved."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False            



class Cave(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "cave"
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["ruins"] = self
        self.verbs["leave"] = self
        

        self.special_item = None
        self.item_collected = False
        self.puzzle_solved = False

    def enter(self):
        if not self.item_collected and not self.puzzle_solved:
            announce(
                "You enter a dark cave, and you are provided with a puzzle to solve."
            )
            self.item_collected = True
            self.start_puzzle()
        elif not self.puzzle_solved:
            announce(
                "The cave, now less intimidating with the special item in your possession, still holds the unsolved puzzle."
            )
            self.start_puzzle()
        else:
            announce(
                "The cave is silent now and everything here is explored."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False


    def start_puzzle(self):
        announce("You find a mysterious inscription on the cave wall: 'What has keys but can't open locks?'")
        self.solve_puzzle()

    def solve_puzzle(self):
        max_guess = 3
        while max_guess != 0:
            announce(f"You have {max_guess} chance(s) to solve it")
            player_answer = input("Your answer: ").strip().lower()
            if player_answer == "keyboard":
                announce("Correct! The cave reveals its secrets.")
                self.puzzle_solved = True
                max_guess = 0
                announce(
                    "As you answer correctly, a hidden passage reveals itself, leading deeper into the cave."
                )
                announce("You explore the passage and find a treasure before leaving the cave.")
            else:
                announce("That's not right. Think carefully and try again.")
                max_guess -= 1
                announce(f"{max_guess} chance(s) left.")
                if max_guess == 0:
                    announce("YOU LOST! LEAVE THE CAVE!")

class Ruins(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "ruins"  
        self.verbs["beach"] = self
        self.verbs["forest"] = self
        self.verbs["cave"] = self
        self.verbs["cliff"] = self
        self.verbs["leave"] = self

        self.treasure_collected = False

    def enter(self):
        if not self.treasure_collected:
            announce(
                "You step into a big castle ruin. You explore around and find dead skeletons of animals. You get attacked by zombies of dead pirates."
            )
            self.treasures = items.Treasure("Ruby", 100)
            self.treasure_collected = True
            announce("You have found a big amount of gold and silver to renovate your ship. Your ship is going to look luxurious.")
            self.events.append(drowned_pirates.DrownedPirates())
        else:
            announce("You have been to the ruins and fought the dead pirates. You probably wouldn't want to go there.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "beach":
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "forest":
            config.the_player.next_loc = self.main_location.locations["forest"]
        if verb == "cave":
            config.the_player.next_loc = self.main_location.locations["cave"]
        if verb == "cliff":
            config.the_player.next_loc = self.main_location.locations["cliff"]
        if verb == "ruins":
            config.the_player.next_loc = self.main_location.locations["ruins"]
        if verb == "leave":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
