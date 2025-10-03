from __future__ import annotations

import operator

import random_gen
import pokemon
from array_sorted_list import ArraySortedList
from bset import BSet
from queue_adt import CircularQueue
from referential_array import ArrayR
from sorted_list import ListItem
from stack_adt import ArrayStack

"""
the implementation of a pokemon team
"""
__author__ = "Scaffold by Jackson Goerner, Code by Yin Lam Lo"

from enum import Enum, auto
from pokemon_base import PokemonBase, Status


def get_generate_order():
    ''' return a list of pokedex order '''
    team_default_order = ArraySortedList(5)
    team_default_order.add(ListItem(pokemon.Charmander(), 0))
    team_default_order.add(ListItem(pokemon.Bulbasaur(), 2))
    team_default_order.add(ListItem(pokemon.Squirtle(), 4))
    team_default_order.add(ListItem(pokemon.Gastly(), 6))
    team_default_order.add(ListItem(pokemon.Eevee(), 9))
    return team_default_order

def get_pokedex_reverse_order(poke: PokemonBase) -> int:
    """
    return the order number of the pokemon from large to small
    :best-case complexity:   O(1)
    :worst-case complexity:  O(1)
    :pre:   poke must be PokemonBase
    """
    if type(poke) is pokemon.Charmander:
        return 9
    if type(poke) is pokemon.Charizard:
        return 8
    if type(poke) is pokemon.Bulbasaur:
        return 7
    if type(poke) is pokemon.Venusaur:
        return 6
    if type(poke) is pokemon.Squirtle:
        return 5
    if type(poke) is pokemon.Blastoise:
        return 4
    if type(poke) is pokemon.Gastly:
        return 3
    if type(poke) is pokemon.Haunter:
        return 2
    if type(poke) is pokemon.Gengar:
        return 1
    if type(poke) is pokemon.Eevee:
        return 0

# bm0: stack, bm1: queue, bm2: sorted_list (according to criterion)
def get_empty_team(team_size, battle_mode):
    """
    return an empty according to battle mode
    :best-case complexity:   O(1)
    :worst-case complexity:  O(1)
    """
    if battle_mode == 0:
            team_members = ArrayStack(team_size)
    elif battle_mode == 1:
            team_members = CircularQueue(team_size)
    elif battle_mode == 2:
            team_members = ArraySortedList(team_size)
    return team_members


class Action(Enum):
    ATTACK = auto()
    SWAP = auto()
    HEAL = auto()
    SPECIAL = auto()


class Criterion(Enum):
    SPD = auto()
    HP = auto()
    LV = auto()
    DEF = auto()


class ORDER(Enum):
    INCREASING = auto()
    DECREASING = auto()


class PokeTeam:
    class AI(Enum):
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()

    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None,
                 criterion_value=None) -> None:
        """
        constructor for a poke team
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if type(team_name) is not str:
            raise TypeError("param team_name must be str")
        if type(team_numbers) is not list:
            raise TypeError("param team_number must be list")
        if type(battle_mode) is not int:
            raise TypeError("param battle_mode must be int")
        if type(ai_type) is not PokeTeam.AI:
            raise TypeError("param ai_type must be PokeTeam.AI")
        if battle_mode == 2:
            if type(criterion) is not Criterion:
                raise TypeError("param criterion must be PokeTeam.Criterion for battle mode 2")
        # FIT1008 could ignore the use of criterion_value

        self.team_name = team_name
        self.battle_mode = battle_mode
        self.criterion = criterion
        self.ai_type = ai_type
        self.team_members = None
        self.team_numbers = team_numbers
        self.criterion_value = criterion_value
        self.display_order = ORDER.DECREASING
        self.heal_attempt = 3
        self.regenerate_team()

    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs) -> None:
        """
        class method for generaring a random team
        :best-case complexity:   O(1)
        :worst-case complexity:  O(n)
        there is a loop loop that will only run for 4 times so its constant,
        we only calculate the loop that could change
        """
        max_team_size = 6
        if team_size is None:   # random team size between half of the team to max
            team_size = random_gen.RandomGen.randint(max_team_size // 2, max_team_size)
        team_num = ArraySortedList(team_size)
        team_num.add(ListItem(0, 0))
        team_num.add(ListItem(team_size, team_size))  # create a team and add 0 and 4 to it
        for i in range(4):  # add 4 random values
            rand_value = random_gen.RandomGen.randint(0, team_size)
            team_num.add(ListItem(rand_value, rand_value))
        team_numbers = []
        for i in range(len(team_num) - 1):  # adding pokemon amount to the list
            team_numbers.append(team_num.__getitem__(i + 1).value - team_num.__getitem__(i).value)

        if ai_mode is None:                 # if ai mode is empty, set it as random
            ai_mode = PokeTeam.AI.RANDOM

        if "criterion" in kwargs.keys():
            criterion = kwargs["criterion"]
        else:
            criterion = None

        # criterion_value can be ignore for FIT1008
        criterion_value = 0

        # return a generated team to init
        return cls(team_name, team_numbers, battle_mode, ai_mode, criterion, criterion_value)

    def get_team_name(self) -> str:
        """
        return the team name
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.team_name

    def return_pokemon(self, poke: PokemonBase) -> None:
        """
        return the pokemon to the team from the field according to the battle mode for different ADTs
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        poke.set_status(Status.NO_STATUS)
        if poke.is_fainted():   # fainted pokemon should not return to the team
            return
        if self.battle_mode == 0:
            self.team_members.push(poke)
        elif self.battle_mode == 1:
            self.team_members.append(poke)
        elif self.battle_mode == 2:
            # sort above tens digit: criterion value
            # if criterion value is the same (i.e. key // 10) => determine of pokedex value (i.e. single digit)
            if self.criterion == Criterion.SPD:
                self.team_members.add(ListItem(poke, poke.get_speed() * 10 + get_pokedex_reverse_order(poke)))
            elif self.criterion == Criterion.HP:
                self.team_members.add(ListItem(poke, poke.get_hp() * 10 + get_pokedex_reverse_order(poke)))
            elif self.criterion == Criterion.LV:
                 self.team_members.add(ListItem(poke, poke.get_level() * 10 + get_pokedex_reverse_order(poke)))
            elif self.criterion == Criterion.DEF:
                self.team_members.add(ListItem(poke, poke.get_defence() * 10 + get_pokedex_reverse_order(poke)))

    def retrieve_pokemon(self) -> PokemonBase | None:
        """
        retrieve pokemon out of the team to the field for different ADTs
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if self.battle_mode == 0:
            retrieved = self.team_members.pop()
        elif self.battle_mode == 1:
            retrieved = self.team_members.serve()
        elif self.battle_mode == 2:
            # adjust to battle mode 2 special
            if self.display_order is ORDER.DECREASING:
                retrieved = self.team_members.delete_at_index(len(self.team_members)-1).value
            else:
                retrieved = self.team_members.delete_at_index(0).value  # since it is reversed

        return retrieved

    def special(self) -> None:
        """
        operate the special action with different ADTs
        :best-case complexity:   O(1) for mode 2
        :worst-case complexity:  O(2n) for mode 0 and 1 with 2 loops
        """
        if self.battle_mode == 0:
            # swaps the first and last pokemon
            if len(self.team_members) != 1:     # if team member not only have one left
                temp = ArrayStack(len(self.team_members))   # stack is used for bm0 so we need a new stack to put pokemon that is in the middle
                first = self.team_members.pop()             # get the first one out first
                for i in range(len(self.team_members) - 1): # get the middle ones out in the temp stack
                    temp.push(self.team_members.pop())
                last = self.team_members.pop()              # get the last one out
                self.team_members.push(first)               # put the first one in the stack
                for i in range(len(temp)):                  # out the middle ones back in
                    self.team_members.push(temp.pop())
                self.team_members.push(last)                # put the last one at top
        elif self.battle_mode == 1:
            temp = ArrayStack(len(self.team_members))       # make temp stack and push the first half of the queue to it
            for i in range(len(self.team_members) // 2):
                temp.push(self.team_members.serve())
            for i in range(len(temp)):                      # that the top of the stack and insert it to the queue
                this = temp.pop()
                self.team_members.append(this)
        elif self.battle_mode == 2:                         # switch the ordering and make other part function adjust to it
            if self.display_order is ORDER.DECREASING:
                self.display_order = ORDER.INCREASING
            elif self.display_order is ORDER.INCREASING:
                self.display_order = ORDER.DECREASING

    def regenerate_team(self) -> None:
        """
        insert the pokemon according to its ADT to it follows the pokedex order required
        :best-case complexity:   O(1)       with only 1 member in team list
        :worst-case complexity:  O(n^2)     2 loops
        """
        self.team_members = get_empty_team(sum(self.team_numbers), self.battle_mode)
        if self.battle_mode == 0 or self.battle_mode == 2:
            for i in range(len(self.team_numbers) - 1, -1, -1):     # insert it from the largest pokedex value
                for j in range(self.team_numbers[i]):
                    self.return_pokemon(get_generate_order()[i].value)
        elif self.battle_mode == 1:
            for i in range(len(self.team_numbers)):                 # insert it from the smallest pokedex value
                for j in range(self.team_numbers[i]):
                    self.return_pokemon(get_generate_order()[i].value)
        if self.battle_mode == 2:
            self.display_order = ORDER.DECREASING
        self.heal_attempt = 3

    def __str__(self) -> str:
        """
        print the team in organised str
        :best-case complexity:   O(1)   for mode 0 and 1
        :worst-case complexity:  O(n)   for mode 2 loop str generation
        """
        if self.battle_mode == 0:
            return_str = "{} ({}): {}".format(self.team_name, self.battle_mode, self.team_members)
        if self.battle_mode == 1:
            return_str = "{} ({}): {}".format(self.team_name, self.battle_mode, self.team_members)
        if self.battle_mode == 2:
            # adjust to battle mode 2 special
            if self.display_order is ORDER.DECREASING:
                return_str = "{} ({}): [".format(self.team_name, self.battle_mode)
                for i in range(len(self.team_members)-1, -1, -1):
                    return_str += str(self.team_members.__getitem__(i).value)
                    if i != 0:
                        return_str += ", "
                return_str += "]"
            else:
                return_str = "{} ({}): [".format(self.team_name, self.battle_mode)
                for i in range(len(self.team_members)):
                    return_str += str(self.team_members.__getitem__(i).value)
                    if i != len(self.team_members)-1:
                        return_str += ", "
                return_str += "]"
        return return_str

    def get_ai_type(self) -> AI:
        """
        return the ai_type of the team
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.ai_type

    def is_empty(self) -> bool:
        """
        is the team is empty of not
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        return self.team_members.is_empty()

    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        """
        get the action depending on the AI or user input
        :best-case complexity:   O(1) for any action besides user input
        :worst-case complexity:  O(n) for user input
        """
        if self.ai_type is self.AI.ALWAYS_ATTACK:
            return Action.ATTACK
        elif self.ai_type is self.AI.SWAP_ON_SUPER_EFFECTIVE:
            if their_pokemon.get_damage_multiplier(my_pokemon) >= 1.5:
                return Action.SWAP
            else:
                return Action.ATTACK
        elif self.ai_type is self.AI.RANDOM:
            action_list = list(Action)  # determine by random selecting
            if self.heal_attempt == 0:
                action_list.remove(Action.HEAL)
            return action_list[random_gen.RandomGen.randint(0, len(action_list) - 1)]
        elif self.ai_type is self.AI.USER_INPUT:
            print("A [ATTACK], P [POKEMON], H [HEAL], S [SPECIAL]")
            while True:
                option = input("Select your action:")
                if option == 'A':
                    return Action.ATTACK
                elif option == 'P':
                    return Action.SWAP
                elif option == 'H':
                    if self.heal_attempt > 0:
                        return Action.HEAL
                    else:
                        print("You healed for 3 times already.")
                        return 0
                elif option == 'S':
                    return Action.SPECIAL

    def heal_action(self, poke: PokemonBase):
        """
        heal the pokemon and reduce one heal attempt
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        poke.heal();
        self.heal_attempt -= 1

    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()
    # could ignore because its worth no marks

    def get_team_members(self):
        """
                :best-case complexity:   O(1)
                :worst-case complexity:  O(1)
        """
        return self.team_members

