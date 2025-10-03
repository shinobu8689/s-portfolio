from __future__ import annotations

from cave import Cave
from heap import MaxHeap
from material import Material
from random_gen import RandomGen
from trader import Trader
from food import Food
from hash_table import LinearProbeTable
from bst import BinarySearchTree

# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]


class Player():
    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        '''
             Initialises a player with name and how many emerald it owns
             Parameters: name (str), emeralds (float)
             Return:     None
             Complexity: O(1)
        '''
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.traders = None
        self.foods = None
        self.materials = None
        self.caves = None
        self.temp_caves = None

    def set_traders(self, traders_list: list[Trader]) -> None:
        '''
            set available trader to player attribute for player to access trades
            Parameters: traders_list (list[Trader])
            Return:     None
            Complexity: O(Trader)
        '''
        self.traders = LinearProbeTable(len(traders_list), -1)
        for trader in traders_list:  # O(traders)
            # take the material that the trader is selling
            if not trader.is_currently_selling():
                if len(trader.inventory) > 0:
                    trader.generate_deal()
            if trader.is_currently_selling():
                if trader.CurrentDeal[0].name in self.traders:
                    current_trader = self.traders[trader.CurrentDeal[0].name]
                    if current_trader.CurrentDeal[1] < trader.CurrentDeal[1]:
                        del self.traders[trader.CurrentDeal[0].name]
                        self.traders[trader.CurrentDeal[0].name] = trader
                else:
                    self.traders[trader.CurrentDeal[0].name] = trader

    def set_foods(self, foods_list: list[Food]) -> None:
        '''
            set accessible food that the player could have
            Parameters: foods_list (list[Food])
            Return:     None
            Complexity: O(1)
        '''
        self.foods = foods_list

    @classmethod
    def random_player(cls) -> Player:
        '''
            Generate a random player based on the provided name list
            Parameters: None
            Return:     Player object
            Complexity: O(1)
        '''
        return cls(PLAYER_NAMES[RandomGen.randint(0, len(PLAYER_NAMES) - 1)])

    def set_materials(self, materials_list: list[Material]) -> None:
        '''
            set material to player
            Parameters: materials_list (list[Material])
            Return:     None
            Complexity: O(1)
        '''
        self.materials = materials_list

    def set_caves(self, caves_list: list[Cave]) -> None:
        '''
            set accessible cave to player
            Parameters: caves_list (list[Cave])
            Return:     None
            Complexity: O(C*logC)
        '''
        self.temp_caves = caves_list
        self.caves = MaxHeap(len(caves_list))
        count = 0
        for cave in caves_list:  # O(caves)
            count += 0.0000000001
            self.caves.add(cave.quantity + count / cave.material.mining_rate, cave)

    def get_traders(self) -> LinearProbeTable:
        '''
            return the trader attribute
            Parameters: None
            Return:     LinearProbeTable
            Complexity: O(1)
        '''
        return self.traders

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
        """
            select the most optimal action that the player should de
            Parameters: None
            Return:     tuple(food, current_balance, cave_visited)
            :raises     ValueError: could not proceed when traders, foods, materials, caves is empty
            Complexity: O(T+F*C*logC)

            Description:

            The strategy that we use for this part of the project to overcome the requirements is that
            we iterate through the food to find the best food value for the trip. Each iteration of food,
            we would check if the player is able to buy that food, if yes we would take the hunger given by
            that food and subtract the balance with the price of that food then while there is still caves
            that are not empty and we still have the hunger to mine, we will find the most optimal cave
            By simply using the get_max function in MaxHeap. Then we mine the cave, get the materials,
            and trade it with the trader. And for every cave we visited, we will put this cave inside in an
            array which are all the caves that that player visited in a day for every iteration of food. if the
            balance return for this iteration of food is the highest compared to other food, we will use this food
            and return the food, balance, and the caves visited.

            our initial plan was to include the materials sold by the traders and the price point that they are selling at
            however we were not able to meet the complexity requirement using this strategy, therefore we will only
            rely on the cave informations to get the most optimal cave to mine, further details is written below

            Finding the most optimal cave :

            To find the most optimal cave, we store the caves within a MaxHeap,
            with the cave object as the item and the (quantity of material inside the cave/the material mining rate) as the key.
            Retrieving the maximum key which also indicates the most number material that can be mined while
            taking the least amount of hunger complexity is O(1) which is efficient for the complexity requirement
            for this function. The cave returned by this this just enough to obtain the required balance at the
            end of the day that is written in the test cases.
            This is coded within the set_caves method

            =========================================================================================================================

            complexity analysis:

            setting the traders                                    O(T)
            we iterate every food                                  O(F)
                every food, while there is still cave, keep mining O(C*logC)
                finding the most optimal cave                      O(1)

            total complexity = O(T + F*C*logC)

            =======================================================================================================================

            worked examples:
                scenario:
                    materials, mining rate(hunger/item):
                        - ("Gold Nugget", 27.24)
                        - ("Netherite Ingot", 20.95)
                        - ("Fishing Rod", 26.93)
                        - ("Ender Pearl", 13.91)
                        - ("Prismarine Crystal", 11.48)

                    caves:
                        -("Boulderfall Cave", prismarine, 10),
                        -("Castle Karstaag Ruins", netherite, 4),
                        -("Glacial Cave", gold, 3),
                        -("Orotheim", fishing_rod, 6),
                        -("Red Eagle Redoubt", fishing_rod, 3),

                    traders:
                        - RandomTrader("Waldo Morgan"), fishing_rod: 7.57 💎
                        - RandomTrader("Orson Hoover"), gold:4.87 💎
                        - RandomTrader("Lea Carpenter"), prismarine:5.65 💎
                        - RandomTrader("Ruby Goodman"), netherite:8.54 💎
                        - RandomTrader("Mable Hodge"), gold:6.7 💎

            first mine trip
                current cave:  Boulderfall Cave: Prismarine Crystal: 11.48🍗/💎 - Quantity: 10
                Quantity Mined:  9.233449477351916
                Current Trader:  Lea Carpenter
                Balance:  72.16898954703834

            second mine trip
                current cave:  Boulderfall Cave: Prismarine Crystal: 11.48🍗/💎 - Quantity: 10
                Quantity Mined:  10
                Current Trader:  Lea Carpenter
                Balance:  82.5

            third mine trip
                current cave:  Orotheim: Fishing Rod: 26.93🍗/💎 - Quantity: 6
                Quantity Mined:  0.5272929818046784
                Current Trader:  Waldo Morgan
                Balance:  86.49160787226141

            fourth mine trip
                current cave:  Castle Karstaag Ruins: Netherite Ingot: 20.95🍗/💎 - Quantity: 4
                Quantity Mined:  -8.479030259667066e-17
                Current Trader:  Ruby Goodman
                Balance:  86.49160787226141

            fifth mine trip
                current cave:  Red Eagle Redoubt: Fishing Rod: 26.93🍗/💎 - Quantity: 3
                Quantity Mined:  -7.32325385463249e-33
                Current Trader:  Waldo Morgan
                Balance:  86.49160787226141

            sixth mine trip:
                current cave:  Boulderfall Cave: Prismarine Crystal: 11.48🍗/💎 - Quantity: 10
                Quantity Mined:  10
                Current Trader:  Lea Carpenter
                Balance:  87.5

            seventh mine trip:
                current cave:  Orotheim: Fishing Rod: 26.93🍗/💎 - Quantity: 6
                Quantity Mined:  6
                Current Trader:  Waldo Morgan
                Balance:  132.92000000000002

            eighth mine trip:
                current cave:  Castle Karstaag Ruins: Netherite Ingot: 20.95🍗/💎 - Quantity: 4
                Quantity Mined:  4
                Current Trader:  Ruby Goodman
                Balance:  167.08

            ninth mine trip:
                current cave:  Red Eagle Redoubt: Fishing Rod: 26.93🍗/💎 - Quantity: 3
                Quantity Mined:  2.3698477534348314
                Current Trader:  Waldo Morgan
                Balance:  185.01974749350168

            total balance: 185.01974749350168

        """
        if self.traders is None or self.foods is None or self.materials is None or self.caves is None:
            raise ValueError
        BestFoodChoiceAndCaves = None, self.balance, []

        for food in self.foods:
            if food.price <= self.balance:
                self.set_caves(self.temp_caves)
                hunger_bars = food.hunger_bars
                current_balance = self.balance - food.price
                cave_visited = []

                # print("Current Foood: ", food)
                while not self.caves.is_empty() and hunger_bars != 0:  # O(cave)--> unlikely or O(hunger_bar)
                    OptimalCave = self.caves.get_max()[1]  # O(1)
                    if OptimalCave.material.name in self.traders:
                        trader = self.traders[OptimalCave.material.name]
                        #here we check if we have enough hunger to mine all materials or less hunger so we a=only can mine materials according to our hunger
                        Item_Mined_Qty = min(hunger_bars / OptimalCave.material.mining_rate, OptimalCave.quantity)
                        hunger_bars -= OptimalCave.material.mining_rate * Item_Mined_Qty
                        current_balance += trader.CurrentDeal[1] * Item_Mined_Qty
                        cave_visited.append((OptimalCave, Item_Mined_Qty))

                if BestFoodChoiceAndCaves[1] < current_balance:
                    BestFoodChoiceAndCaves = food, current_balance, cave_visited

        return BestFoodChoiceAndCaves

    def __str__(self) -> str:
        '''
            to_string method
            Complexity: O(1)
        '''
        return self.name + ": $" + str(self.balance)


if __name__ == "__main__":
    pass
