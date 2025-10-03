from __future__ import annotations

import battle
import pokemon
import random_gen
from array_sorted_list import ArraySortedList
from bset import BSet
from linked_list import LinkedList
from poke_team import PokeTeam
from battle import Battle
from queue_adt import CircularQueue
from referential_array import ArrayR
from stack_adt import ArrayStack

"""
the implementation of the battle tower
"""
__author__ = "Scaffold by Jackson Goerner, Code by Yin Lam Lo"

name_list = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliett', 'Kilo',
             'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor',
             'Whiskey', 'X-ray', 'Yankee', 'Zulu']


class BattleTower:

    def __init__(self, battle: Battle | None = None) -> None:
        """
        constructor
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if battle is None:
            battle = Battle(verbosity=0)
        self.battle_sys = battle
        self.tower_team = None
        self.my_team = None

    def set_my_team(self, team: PokeTeam) -> None:
        """
        set the team used in tower
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.my_team = team

    def generate_teams(self, n: int) -> None:
        """
            generate the teams in the tower
            :best-case complexity:   O(1), n = 1
            :worst-case complexity:  O(n)
        """
        if type(n) is not int:
            raise TypeError("param n must be int")

        self.tower_team = CircularQueue(n)

        name_count = 0
        for i in range(n):
            battle_mode = random_gen.RandomGen.randint(0, 1)
            name = name_list[name_count]
            team = PokeTeam.random_team(name, battle_mode)
            lives = random_gen.RandomGen.randint(2, 10)
            team_and_lives = LinkedList()
            team_and_lives.insert(0, team)
            team_and_lives.insert(1, lives)
            self.tower_team.append(team_and_lives)

            print("lt", lives, team)
            name_count += 1

        print("============")


    def __iter__(self):
        """
            start the BattleTowerIterator
            :best-case complexity:   O(1)
            :worst-case complexity:  O(1)
        """
        return BattleTowerIterator(self)


class BattleTowerIterator:

    def __init__(self, battle_tower: BattleTower):
        """
            basic constructor
            :best-case complexity:   O(1)
            :worst-case complexity:  O(1)
        """
        self.battle_tower = battle_tower
        self.battle_seq = 0
        self.end_battle = False

    def __iter__(self):
        """
            :best-case complexity:   O(1)
            :worst-case complexity:  O(1)
        """
        return self

    def __next__(self):
        """
            it goes through the battle once, and return the battle result
            :best-case complexity:   O(B)
            :worst-case complexity:  O(B)
        """
        if self.battle_tower.tower_team.is_empty() or self.end_battle:
            raise StopIteration
        enemy_pack = self.battle_tower.tower_team.serve()
        enemy_team = enemy_pack.__getitem__(0)
        my_team = self.battle_tower.my_team
        print(self.battle_tower.my_team)
        print(enemy_team)

        res = self.battle_tower.battle_sys.battle(my_team, enemy_team)
        remaining_lives = enemy_pack.__getitem__(1)
        enemy_pack.__setitem__(1, remaining_lives)
        if res == 1:
            remaining_lives -= 1
        enemy_pack.clear()
        enemy_pack.insert(0, enemy_team)
        enemy_pack.insert(1, remaining_lives)

        if res == 2:
            self.end_battle = True

        self.battle_tower.tower_team.append(enemy_pack)

        return res, self.battle_tower.my_team.regenerate_team(), enemy_team, remaining_lives

    def avoid_duplicates(self):
        """
            required complexity
            :best-case complexity:   O(N*P)
            :worst-case complexity:  O(N*P)
        """
        print("==========")
        N = len(self.battle_tower.tower_team)

        while N > 0 :
            current_pack = self.battle_tower.tower_team.serve()
            current_team = current_pack.__getitem__(0)
            C = 0
            B = 0
            S = 0
            G = 0
            E = 0
            if current_team.battle_mode == 0:
                temp_stack = ArrayStack(len(current_team.get_team_members()))
                for P in range(len(current_team.get_team_members())):
                    poke = current_team.retrieve_pokemon()
                    if type(poke) is pokemon.Charmander:
                        C += 1
                    if type(poke) is pokemon.Bulbasaur:
                        B += 1
                    if type(poke) is pokemon.Squirtle:
                        S += 1
                    if type(poke) is pokemon.Gastly:
                        G += 1
                    if type(poke) is pokemon.Eevee:
                        E += 1
                    temp_stack.push(poke)
                if not temp_stack.is_empty():       # its ugly but its achieve the complexity
                    current_team.return_pokemon(temp_stack.pop())
                if not temp_stack.is_empty():
                    current_team.return_pokemon(temp_stack.pop())
                if not temp_stack.is_empty():
                    current_team.return_pokemon(temp_stack.pop())
                if not temp_stack.is_empty():
                    current_team.return_pokemon(temp_stack.pop())
                if not temp_stack.is_empty():
                    current_team.return_pokemon(temp_stack.pop())
                if not temp_stack.is_empty():
                    current_team.return_pokemon(temp_stack.pop())

            elif current_team.battle_mode == 1:
                for P in range(len(current_team.get_team_members())):
                    poke = current_team.retrieve_pokemon()
                    if type(poke) is pokemon.Charmander:
                        C += 1
                    if type(poke) is pokemon.Bulbasaur:
                        B += 1
                    if type(poke) is pokemon.Squirtle:
                        S += 1
                    if type(poke) is pokemon.Gastly:
                        G += 1
                    if type(poke) is pokemon.Eevee:
                        E += 1
                    current_team.return_pokemon(poke)
            elif current_team.battle_mode == 2:
                for P in range(len(current_team.get_team_members())):
                    poke = current_team.team_member.__getitem__(P)
                    if type(poke) is pokemon.Charmander:
                        C += 1
                    if type(poke) is pokemon.Bulbasaur:
                        B += 1
                    if type(poke) is pokemon.Squirtle:
                        S += 1
                    if type(poke) is pokemon.Gastly:
                        G += 1
                    if type(poke) is pokemon.Eevee:
                        E += 1
            if not (C > 1 or B > 1 or S > 1 or G > 1 or E > 1):
                self.battle_tower.tower_team.append(current_pack)
            N -= 1

        print("****")
        for i in range(len(self.battle_tower.tower_team)):
            a = self.battle_tower.tower_team.serve()
            print(a.__getitem__(0))
            self.battle_tower.tower_team.append(a)
        print("****")


    def sort_by_lives(self):
        # 1054
        raise NotImplementedError()
