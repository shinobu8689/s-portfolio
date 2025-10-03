from __future__ import annotations

from heap import MaxHeap
from player import Player
from trader import Trader, RandomTrader
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen
from hash_table import LinearProbeTable


class Game:
    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5

    def __init__(self) -> None:
        '''
             Initialises a game object
             Parameters: None
             Return:     None
             Complexity: O(1)
        '''
        self.temp_caves = None
        self.materials = None
        self.caves = None
        self.traders = None
        self.food = None
        self.temp_traders = None

    def initialise_game(self) -> None:
        """Initialise all game objects: Materials, Caves, Traders."""
        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        print("Materials:\n\t", end="")
        print("\n\t".join(map(str, self.get_materials())))
        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        print("Caves:\n\t", end="")
        print("\n\t".join(map(str, self.get_caves())))
        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        print("Traders:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]):
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)

    def set_materials(self, mats: list[Material]) -> None:
        self.materials = mats

    def set_caves(self, caves: list[Cave]) -> None:
        self.caves = caves

    def set_traders(self, traders: list[Trader]) -> None:
        '''
            set available trader to player attribute for player to access trades
            Parameters: traders_list (list[Trader])
            Return:     None
            Complexity: O(Trader)
        '''
        self.temp_traders = LinearProbeTable(len(traders), -1)
        self.traders = traders
        for trader in traders:  # O(traders)
            # take the material that the trader is selling
            if not trader.is_currently_selling():
                if len(trader.inventory) > 0:
                    trader.generate_deal()
            if trader.is_currently_selling():
                if trader.CurrentDeal[0].name in self.temp_traders:
                    current_trader = self.temp_traders[trader.CurrentDeal[0].name]
                    if current_trader.CurrentDeal[1] < trader.CurrentDeal[1]:
                        del self.temp_traders[trader.CurrentDeal[0].name]
                        self.temp_traders[trader.CurrentDeal[0].name] = trader
                else:
                    self.temp_traders[trader.CurrentDeal[0].name] = trader

    def get_materials(self) -> list[Material]:
        return self.materials

    def get_caves(self) -> list[Cave]:
        return self.caves

    def get_traders(self) -> list[Trader]:
        return self.traders

    def remove_caves(self, traders: LinearProbeTable) -> None:
        '''
        removes caves that contain materials that are currently not being traded by any trader.
        best case complexity = worst case complexity = O(C*logC)
        '''
        self.temp_caves = MaxHeap(len(self.caves))
        count = 0
        for cave in self.caves:                                             # O(C)
            if cave.material.name in traders:
                count += 0.0000000001
                ratio = cave.quantity + count / cave.material.mining_rate
                self.temp_caves.add(ratio, cave)                            # O(LogC)


    def generate_random_materials(self, amount) -> list[Material]:
        """
        Generates <amount> random materials using Material.random_material
        Generated materials must all have different names and different mining_rates.
        (You may have to call Material.random_material more than <amount> times.)
            Parameters: amount (int)
            Return:     list[Material]
            Complexity: O(amount)
        """
        material_list = []
        next_material = Material.random_material()
        material_list.append(next_material)

        while len(material_list) < amount:
            next_material = Material.random_material()
            is_duplicate = False
            for i in material_list:
                if i.name == next_material.name or i.mining_rate == next_material.mining_rate:
                    is_duplicate = True
                    break
            if not is_duplicate:
                material_list.append(next_material)
        self.materials = material_list

    def generate_random_caves(self, amount) -> list[Cave]:
        """
        Generates <amount> random caves using Cave.random_cave
        Generated caves must all have different names
        (You may have to call Cave.random_cave more than <amount> times.)
            Parameters: amount (int)
            Return:     list[Cave]
            Complexity: O(amount)
        """
        cave_list = []
        next_cave = Cave.random_cave(self.materials)
        cave_list.append(next_cave)

        while len(cave_list) < amount:
            next_cave = Cave.random_cave(self.materials)
            is_duplicate = False
            for i in cave_list:
                if i.name == next_cave.name:
                    is_duplicate = True
                    break
            if not is_duplicate:
                cave_list.append(next_cave)
        self.caves = cave_list

    def generate_random_traders(self, amount) -> list[Trader]:
        """
        Generates <amount> random traders by selecting a random trader class
        and then calling <TraderClass>.random_trader()
        and then calling set_all_materials with some subset of the already generated materials.
        Generated traders must all have different names
        (You may have to call <TraderClass>.random_trader() more than <amount> times.)
            Parameters: amount (int)
            Return:     list[Trader]
            Complexity: O(amount)
        """
        trader_list = []
        next_trader = RandomTrader.random_trader()
        trader_list.append(next_trader)

        while len(trader_list) < amount:
            next_trader = RandomTrader.random_trader()
            is_duplicate = False
            for i in trader_list:
                if i.name == next_trader.name:
                    is_duplicate = True
                    break
            if not is_duplicate:
                trader_list.append(next_trader)

        for i in range(len(trader_list)):
            inventory_list = []
            for j in range(RandomGen.randint(4, 16)):
                inventory_list.append(self.materials[RandomGen.randint(0, len(self.materials) - 1)])
            trader_list[i].set_all_materials(inventory_list)
            trader_list[i].generate_deal()

        self.traders = trader_list

    def finish_day(self):
        """
        DO NOT CHANGE
        Affects test results.
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2):
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else:
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)


class SoloGame(Game):

    def initialise_game(self) -> None:
        """Initialise all game objects: Materials, Caves, Traders."""
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader],
                             player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def simulate_day(self):
        # 1. Traders make deals
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD)
        foods = []
        for _ in range(food_num):
            foods.append(Food.random_food())
        print("\nFoods:\n\t", end="")
        print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)
        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()
        print(food, balance, caves)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)

    def verify_output_and_update_quantities(self, food: Food | None, balance: float,
                                            caves: list[tuple[Cave, float]]) -> None:
        '''
             verify the correctness of the output and update the quantity in caves
             Parameters: food (Food). balance (float), caves (list[tuple[Cave, float]]))
             Return:     None
             best case = worst case complexity: O(C) (complexity is 3C which simplifies to C)
        '''
        verify_balance = 0
        # 1. Checks that the result makes sense - That:
        # a. Quantities are in line with what the player provided
        for i in range(len(caves)):
            if caves[i][0].quantity < caves[i][1]:
                raise Exception("Cave quantities do not align")
        # b. The food is purchasable, check food is in player.foods
        if food is not None:
            if self.player.balance < food.price:
                raise Exception("Food is not purchasable!")

            # c. The remaining balance is correct, proceed if the balance after the move is valid.
            verify_balance = self.player.balance - food.price
            for i in range(len(caves)):
                trader = self.player.traders[caves[i][0].material.name]
                verify_balance += trader.CurrentDeal[1] * caves[i][1]

            if verify_balance != balance:
                raise Exception("Balance does not match")

        # d. Any other sanity checks you can think of (if there is any)

        # 2. Updates the quantities within each cave accordingly.
        self.player.balance = verify_balance

        for cave in self.caves:
            for i in range((len(caves))):
                if cave == caves[i][0]:
                    cave.quantity -= caves[i][1]


class MultiplayerGame(Game):
    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        '''
             Initialises a game object
             Parameters: None
             Return:     None
             Complexity: O(1)
        '''
        super().__init__()
        self.players = []

    def initialise_game(self) -> None:
        """Initialise all game objects: Materials, Caves, Traders."""
        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players:
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        self.remove_caves(self.temp_traders)
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def generate_random_players(self, amount) -> None:
        """
        Generate <amount> random players. Don't need anything unique, but you can do so if you'd like.
        Complexity: O(amount)
        """
        player_list = []
        for i in range(amount):
            player_list.append(Player.random_player())
        self.players = player_list


    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader],
                             player_names: list[int], emerald_info: list[float]):
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info):
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        self.remove_caves(self.temp_traders)
        print("Players:\n\t", end="")
        print("\n\t".join(map(str, self.players)))

    def simulate_day(self):
        # 1. Traders make deals
        print("Traders Deals:\n\t", end="")
        print("\n\t".join(map(str, self.get_traders())))
        # 2. Food is offered
        offered_food = Food.random_food()
        print(f"\nFoods:\n\t{offered_food}")
        # 3. Each player selects a cave - The game does this instead.
        self.remove_caves(self.temp_traders)
        foods, balances, caves = self.select_for_players(offered_food)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)

    def select_for_players(self, food: Food) -> tuple[list[Food | None], list[float], list[tuple[Cave, float] | None]]:
        """
        selects the most optimal cave for each player to mine based on mining rate/quantity of the material in the cave
        parameter: food - the food selection for the day
        return: list[Food | None] - the food each player selected
                list[float] - the balances of each player after mining a cave
                list[tuple[Cave, float] | None]] - the quantity mined from each cave, or none
        complexity:
        P = the number of players and C = the number of caves
        best case = P, when no players can afford the food
        worst case complexity = PlogC, when all players can afford the food
        ================================================================================================================
        justification:

        to meet the complexity requirements, a max_heap of all the caves available in the multiplayer game is generated
        during game initialisation. this heap is filtered to only include caves materials that traders are buying. this
        means that only caves it would be "valuable" to mine are available to mine. the hashtable of traders available
        is used to search for the specific trader to trade with. a hashtable was used to make searching O(1) complexity
        and help meet the overall complexity requirement. cave selection and trading for each player is therefore
        implemented in logC. this is repeated for every player, making the worst case complexity of this method PlogC.
        ================================================================================================================
        EXAMPLE:

        players:
        alexey - $50
        jackson - $14
        saksham - $35
        brendon - $44

        traders:
        waldo morgan buying fishing rod: 26.93 for 8.9
        orson hoover buying gold nugget: 27.24 for 9.93
        lea carpenter buying prismarine crystal: 11.48 for 8.99
        ruby goodman buying netherite ingot: 20.95 for 5.06
        mable hudge buying gold nugget: 27.24 for 7.65

        food:
        cooked chicken cuts: $19 hunger: 100

        caves:
        boulderfall cave: prismarine crystal, quantity: 10
        castle karstaag ruins: netherite ingot, quantity: 4
        glacial cave: gold nugget, quantity: 3
        orotheim: fishing rod, quantity: 6
        red eagle redoubt: fishing rod, quantity: 3

        self.temp_caves -
        caves ordered the following way: boulderfall cave -> orotheim -> castle karstaag ruins -> red eagle doubt ->
        glacial caves

        self.temp_traders -
        contains: waldo, orson, lea, ruby

        player cave selection (1):
        a. alexey buys food (balance now 31)
        b. goes to boulderfall cave and mines 8.710801.. prismarine crystals
        c. trades with lea carpenter for 8.99 per prismarine crystal
        d. final balance 109.31010...

        player cave selection (2):
        a. jackson cannot afford the food
        b. final balance 14

        player cave selection (3):
        a. saksham buys the food (balance now 16)
        b. goes to orotheim and mines 3.7133... fishing rods
        c. trades with waldo morgan for 8.9 per fishing rod
        d. final balance 49.048644...

        player cave selection (4):
        a. brendon buys the food (balance now 25)
        b. goes to castle karstaag ruins and mines 4 netherite ingots
        c. trades with  ruby for 5.06 per netherite ingot
        d. final balance 45.23999...

        """
        food_bought = []                                                                            # O(1)
        emeralds = []                                                                               # O(1)
        caves_visited = []                                                                          # O(1)
        for player in self.players:                                                             # O(P)
            balance = player.balance                                                                # O(1)
            if balance >= food.price:                                                               # O(comp)
                if len(self.temp_caves) > 0:                                                        # O(comp)
                    cave = self.temp_caves.get_max()[1]                                         # O(logC)
                    food_bought.append(food)                                                        # O(1)
                    hunger_bars = food.hunger_bars                                                  # O(1)
                    balance -= food.price                                                           # O(1)
                    trader = player.traders[cave.material.name]                                     # O(1)
                    mined_quantity = min(hunger_bars / cave.material.mining_rate, cave.quantity)    # O(1)
                    hunger_bars -= cave.material.mining_rate * mined_quantity                       # O(1)
                    balance += trader.CurrentDeal[1] * mined_quantity                               # O(1)
                    caves_visited.append([cave, mined_quantity])                                    # O(1)

                else:   # O(1)
                    balance = player.balance
                    food_bought.append(None)
                    caves_visited.append(None)
            else:   # O(1)
                balance = player.balance
                food_bought.append(None)
                caves_visited.append(None)
            emeralds.append(balance)    # O(1)
        return food_bought, emeralds, caves_visited

    def verify_output_and_update_quantities(self, foods: Food | None, balances: float,
                                            caves: list[tuple[Cave, float] | None]) -> None:
        '''
             verify the correctness of the output and update the quantity in caves
             Parameters: food (Food). balance (float), caves (list[tuple[Cave, float]]))
             Return:     None
             best case = worst case complexity: O(Players*Foods*Caves*Balance + Players + Caves)
        '''
        # verifying details make sense
        for i in range(len(self.players)):
            for j in range(len(foods)):
                if i == j:
                    if foods[j] is not None and self.players[i].balance < foods[j].price:
                        raise Exception("Player bought food they could not afford!")
                    for k in range(len(caves)):
                        if i == k:
                            if caves[k] is not None and foods[j] is not None:
                                if caves[k][0].quantity < caves[k][1]:
                                    raise Exception("Player mined more material than the cave had!")
                                if round(caves[k][0].material.mining_rate * caves[k][1], 3) > foods[j].hunger_bars:
                                    raise Exception("Player mined more material than they had energy for!")
                                for l in range(len(balances)):
                                    if i == l:
                                        if foods[j] is None:
                                            if self.players[i].balance != balances[l]:
                                                raise Exception(
                                                    "Player has mined from caves without having purchased food.")
                                        else:
                                            trader = self.players[i].traders[caves[k][0].material.name]
                                            if balances[l] != (self.players[i].balance - foods[j].price) + trader.CurrentDeal[1] * caves[k][1]:
                                                raise Exception("Player balance is incorrect!")
        # updating quantities:
        for i in range(len(self.players)):
            for k in range(len(balances)):
                if i == k:
                    self.players[i].balance = balances[k]

        for cave in self.caves:
            for i in range(len(caves)):
                if caves[i] is not None:
                    if cave == caves[i][0]:
                        cave.quantity -= caves[i][1]


if __name__ == "__main__":
    MultiplayerGame().generate_random_players(5)


    r = RandomGen.seed  # Change this to set a fixed seed.
    RandomGen.set_seed(r)

    g = SoloGame()
    g.initialise_game()

    g.simulate_day()
    g.finish_day()

    g.simulate_day()
    g.finish_day()
