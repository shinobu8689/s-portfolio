from __future__ import annotations

from abc import abstractmethod
from enum import Enum

import random_gen

"""
The base structure of pokemon
"""
__author__ = "Scaffold by Jackson Goerner, Code by Yin Lam Lo"


class PokemonBase:

    # constructor
    def __init__(self, base_hp: int, poke_type: PokeType, new_name: str = "DUMMY", base_level: int = 1, level: int = 1,
                 pre_damage: int = 0, base_att_value: int = 1, base_def_value: int = 1, base_spd_value: int = 1, status: Status = None) -> None:
        # constructor param was added besides base_hp and poke_type
        """
        the constructor for each pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        :pre:   All param must be in the correct datatype
        """

        # check param type for precondition
        if type(base_hp) is not int:
            raise TypeError("param hp must be int")
        if type(poke_type) is not PokeType:
            raise TypeError("param poke_type must be PokeType")
        if type(new_name) is not str:
            raise TypeError("param new_name must be str")
        if type(base_level) is not int:
            raise TypeError("param base_level must be base_level")
        if type(level) is not int:
            raise TypeError("param level must be int")
        if type(pre_damage) is not int:
            raise TypeError("param pre_damage must be int")
        if type(base_att_value) is not int:
            raise TypeError("param base_att_value must be int")
        if type(base_def_value) is not int:
            raise TypeError("param base_def_value must be int")
        if type(base_spd_value) is not int:
            raise TypeError("param base_spd_value must be int")
        if type(status) is not Status:
            raise TypeError("param status must be Status")

        # set all the values
        self.poke_name = new_name
        self.poke_type = poke_type
        self.base_hp = base_hp
        self.max_hp = base_hp
        self.current_hp = base_hp
        self.base_level = base_level
        self.level = level
        self.base_attack_value = base_att_value
        self.base_defence_value = base_def_value
        self.base_speed_value = base_spd_value
        self.current_attack_value = self.base_attack_value
        self.current_defence_value = self.base_defence_value
        self.current_speed_value = self.base_speed_value
        self.next_evolve = None
        self.status = status

    # setters
    def set_status(self, new_status: Status) -> None:
        """
        set the status of the pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        :pre:   new_status must be Status
        """
        self.status = new_status

    # getters
    def get_hp(self) -> int:
        """
        set the status of the pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        ''' reutrn the current hp of the pokemon '''
        return self.current_hp

    def get_attack_damage(self) -> int:
        """
        return the current attack value with level (if any)
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.current_attack_value

    def get_defence(self) -> int:
        """
        return the current defence value with level (if any)
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.current_defence_value

    def get_speed(self) -> int:
        """
        return the current speed value with level (if any)
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if self.get_status() == Status.PARALYSIS:   # paralysis makes it slow down
            return self.current_speed_value // 2
        return self.current_speed_value

    def get_poke_type(self) -> PokeType:
        """
        return the type of the pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.poke_type

    def get_status(self) -> Status:
        """
        return the current status on the pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.status

    def get_level(self) -> int:
        """
        return the current status on the pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.level

    def get_poke_name(self) -> str:
        """
        return the name of the pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.poke_name

    def get_base_level(self) -> int:
        """
        return the the base level the pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.base_level

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        '''
        return the next generation of current pokemon, each pokemon got different evolve version
        complexity changes depend on the implementation, see pokemon.py
        '''
        pass

    # functions

    def is_fainted(self) -> bool:
        """
        return if the pokemon has fainted or not
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.current_hp <= 0

    def level_up(self) -> None:
        """
        level up operation
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.level += 1
        diff = self.max_hp - self.current_hp    # get how many hp it should be after evolve
        self.update_stats()                     # update the spec if the pokemon evolve
        self.current_hp = self.max_hp - diff    # update its new hp

    def lose_hp(self, lost_hp: int) -> None:
        """
        pokemon lost hp according to param
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        :pre:   lost_hp > 0
        """
        self.current_hp -= lost_hp

    def heal(self) -> None:
        """
        heal makes the current pokemon to max and reset its status
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        :pre:   lost_hp > 0
        """
        self.current_hp = self.max_hp
        self.status = Status.NO_STATUS

    def should_evolve(self) -> bool:
        """
        evolve only if they got an evolve version
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        :pre:   lost_hp > 0
        """
        if self.get_evolved_version() is not None:
            return self.level >= self.get_evolved_version().get_base_level()
        else:
            return False

    def can_evolve(self) -> bool:
        """
        determine the pokemon should evolve or not
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return not self.is_fainted() and self.should_evolve()

    @abstractmethod
    def defend(self, damage: int) -> None:
        '''
        determine will the pokemon defence the incoming damage, different pokemon got different defence method
        complexity changes depend on the implementation, see pokemon.py
        '''
        pass

    @abstractmethod
    def update_stats(self) -> None:
        '''
        update pokemon's stats after leveling up, different pokemon got different level enhancement
        complexity changes depend on the implementation, see pokemon.py
        '''
        pass

    def get_damage_multiplier(self, other: PokemonBase) -> float:
        """
        get the multiplier according to type advantages
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        # inbuilt list is allow for simple implementation only
        multiplier = [[1, 2, 0.5, 1, 1], [0.5, 1, 2, 1, 1], [2, 0.5, 1, 1, 1], [1.25, 1.25, 1.25, 2, 0],
                      [1.25, 1.25, 1.25, 0, 1]]

        if self.get_poke_type() == PokeType.FIRE:
            i = 0
        elif self.get_poke_type() == PokeType.GRASS:
            i = 1
        elif self.get_poke_type() == PokeType.WATER:
            i = 2
        elif self.get_poke_type() == PokeType.GHOST:
            i = 3
        elif self.get_poke_type() == PokeType.NORMAL:
            i = 4

        if other.get_poke_type() == PokeType.FIRE:
            j = 0
        elif other.get_poke_type() == PokeType.GRASS:
            j = 1
        elif other.get_poke_type() == PokeType.WATER:
            j = 2
        elif other.get_poke_type() == PokeType.GHOST:
            j = 3
        elif other.get_poke_type() == PokeType.NORMAL:
            j = 4

        return multiplier[i][j]     # get the value from the table

    def attack(self, other: PokemonBase) -> int:
        """
        the operation when attacking
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        damage = self.get_attack_damage()
        # Step 1: Status effects on attack damage / redirecting attacks
        if self.status == Status.BURN:
            damage = damage / 2
        elif self.get_status() == Status.CONFUSION:
            if random_gen.RandomGen.random_chance(0.5):
                other = self
        elif self.get_status() == Status.SLEEP:
            return  # if with sleep status it always fails to attack
        # Step 1.5: Type multipliers
        multiplier_value = self.get_damage_multiplier(other)
        damage = damage * multiplier_value
        damage = int(damage)

        # Step 2: Do the attack
        other.defend(damage)

        # Step 3: Losing hp to status effects
        if self.get_status() == Status.BURN:
            self.lose_hp(1)
        elif self.get_status() == Status.POISON:
            self.lose_hp(3)


        # Step 4: Possibly applying status effects
        if random_gen.RandomGen.random_chance(0.2):
            a_status = None
            if self.get_poke_type() == PokeType.FIRE:
                a_status = Status.BURN
            elif self.get_poke_type() == PokeType.GRASS:
                a_status = Status.POISON
            elif self.get_poke_type() == PokeType.WATER:
                a_status = Status.PARALYSIS
            elif self.get_poke_type() == PokeType.GHOST:
                a_status = Status.SLEEP
            elif self.get_poke_type() == PokeType.NORMAL:
                a_status = Status.CONFUSION
            other.set_status(a_status)

        return damage

    def __str__(self) -> str:
        """
        print the str of the pkm info
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return "LV. {} {}: {} HP".format(self.get_level(), self.get_poke_name(), self.get_hp())


class PokeType(Enum):
    FIRE = 1
    GRASS = 2
    WATER = 3
    GHOST = 4
    NORMAL = 5


class Status(Enum):
    BURN = 1
    POISON = 2
    PARALYSIS = 3
    SLEEP = 4
    CONFUSION = 5
    NO_STATUS = 6
