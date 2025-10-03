from __future__ import annotations

from abc import abstractmethod, ABC
from material import *
from random_gen import RandomGen
from avl import AVLTree
# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]



class Trader(ABC):
    def __init__(self, name: str) -> None:
        '''
            Initialises a Trader, the name
            Parameters: name (str)
            Return:     None
            Complexity: O(1)
        '''
        self.name = name
        self.inventory = []
        self.CurrentDeal = tuple()
        self.sell = None

    @classmethod
    def random_trader(cls) -> Trader:
        '''
            Generate a random trader based on the provided name list
            Parameters: None
            Return:     Trader object
            Complexity: O(1)
        '''
        return cls(TRADER_NAMES[RandomGen.randint(0, len(TRADER_NAMES)-1)])

    def set_all_materials(self, mats: list[Material]) -> None:
        '''
            set the material that the trader sells according to the list
            Parameters: mats (list[Material])
            Return:     None
            Complexity: O(1)
        '''
        self.inventory = mats

    def add_material(self, mat: Material) -> None:
        '''
           append material upon the material list
           Parameters: mats (list[Material])
           Return:     None
           Complexity: O(1)
        '''
        self.inventory.append(mat)

    def is_currently_selling(self) -> bool:
        '''
           return the state of trader is selling or not
           Parameters: None
           Return:     Boolean
           Complexity: O(1)
        '''
        return len(self.CurrentDeal) == 2

        #if len(self.CurrentDeal) == 2:
        #    return True
        #return False

    def current_deal(self) -> tuple[Material, float]:
        '''
            return the current deal in form of tuple
            Parameters: None
            Return:     tuple[Material, float]
            :raises ValueError: there is no item to sell
            Complexity: O(1)
        '''
        if self.is_currently_selling():
            return self.CurrentDeal
        raise ValueError

    @abstractmethod
    def generate_deal(self) -> None:
       pass

    def stop_deal(self) -> None:
        '''
            assign a empty tuple to attribute self.CurrentDeal
            Parameters: None
            Return:     None
            Complexity: O(1)
        '''
        self.CurrentDeal = tuple()

    @abstractmethod
    def __str__(self) -> str:
        pass


class RandomTrader(Trader):
    def __init__(self, name: str) -> None:
        '''
            Initialises a random Trader based on Trader Class
            Complexity: O(1)
        '''
        super().__init__(name)

    def generate_deal(self) -> None:
        '''
            Generate a deal according to trader's inventory
            Complexity: O(1)
        '''
        self.CurrentDeal = (self.inventory[RandomGen.randint(0, len(self.inventory) - 1)], round(2 + 8 * RandomGen.random_float(), 2))

    def __str__(self) -> str:
        '''
            to string method
            Complexity: O(1)
        '''
        if self.CurrentDeal != ():
            return f"<RandomTrader: {self.name} buying [{self.CurrentDeal[0]}] for {self.CurrentDeal[1]}💰>"
        else:
            return f"<RandomTrader: {self.name} buying [{self.CurrentDeal}]>"


class RangeTrader(Trader):
    def __init__(self, name: str) -> None:
        '''
            Initialises a random Trader based on Trader Class
            Parameters: name (str)
            Return:     None
            Complexity: O(1)
        '''
        super().__init__(name)
        self.inventory = AVLTree()

    def set_all_materials(self, mats: list[Material]) -> None:
        '''
           set material to self.inventory according to parameter list
           Parameters: mats (list[Material])
           Return:     None
           Complexity: O(mats)
        '''
        self.inventory = AVLTree()
        for material in mats:
            self.add_material(material)

    def add_material(self, mat: Material) -> None:
        '''
           append new material to current inventory list
           Parameters: mats (Material)
           Return:     None
           Complexity: O(1)
        '''
        self.inventory[mat.mining_rate] = mat

    def generate_deal(self) -> None:
        '''
           Generate deal to sell according to the items in the inventory
           Parameters: None
           Return:     None
           Complexity: O(1)
        '''
        i = RandomGen.randint(0, len(self.inventory) - 1)
        j = RandomGen.randint(i, len(self.inventory) - 1)
        RangeMaterial = self.materials_between(i, j)
        if len(RangeMaterial) > 0:
            self.CurrentDeal = (RangeMaterial[RandomGen.randint(0, len(RangeMaterial) - 1)], round(2 + 8 * RandomGen.random_float(), 2))

    def materials_between(self, i: int, j: int) -> list[Material]:
        '''
           Generate deal to sell according to the items in the inventory
           Parameters: i (int), j (int)
           Return:     MaterialList_Items (list[Material])
           Complexity: O(MaterialList_Keys)
        '''
        MaterialList_Keys = self.inventory.range_between(i, j)
        MaterialList_Items = []
        for Key in MaterialList_Keys:
            MaterialList_Items.append(self.inventory[Key])
        return MaterialList_Items

    def __str__(self) -> str:
        '''
            to_string method
            Complexity: O(1)
        '''
        if self.CurrentDeal != ():
            return f"<RangeTrader: {self.name} buying [{self.CurrentDeal[0]}] for {self.CurrentDeal[1]}💰>"
        else:
            return f"<RangeTrader: {self.name} buying [{self.CurrentDeal}]>"



class HardTrader(Trader):
    def __init__(self, name: str) -> None:
        '''
            Initialises a Hard Trader based on Trader Class
            Parameters: name (str)
            Return:     None
            Complexity: O(1)
        '''
        super().__init__(name)
        self.inventory = AVLTree()

    def set_all_materials(self, mats: list[Material]) -> None:
        '''
            set material to self.inventory according to parameter list
            Parameters: mats (list[Material])
            Return:     None
            Complexity: O(mats)
        '''
        self.inventory = AVLTree()
        for material in mats:
            self.add_material(material)

    def add_material(self, mat: Material) -> None:
        '''
           append new material to current inventory list
           Parameters: mats (Material)
           Return:     None
           Complexity: O(1)
        '''
        self.inventory[mat.mining_rate] = mat

    def generate_deal(self) -> None:
        '''
           Generate deal to sell according to the items in the inventory
           Parameters: None
           Return:     None
           Complexity: O(1)
        '''
        self.CurrentDeal = ((self.inventory.get_max()), round(2 + 8 * RandomGen.random_float(), 2))

    def __str__(self) -> str:
        '''
            to_string method
            Complexity: O(1)
        '''
        if self.CurrentDeal != ():
            return f"<HardTrader: {self.name} buying [{self.CurrentDeal[0]}] for {self.CurrentDeal[1]}💰>"
        else:
            return f"<HardTrader: {self.name} buying [{self.CurrentDeal}]>"


if __name__ == "__main__":
    pass