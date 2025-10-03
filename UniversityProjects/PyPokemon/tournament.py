from __future__ import annotations

from bset import BSet
from pokemon_base import PokeType
from queue_adt import CircularQueue
from stack_adt import ArrayStack

"""
Code of task 6 are incomplete, only partially done, due to non-active teammates
group grief form was submitted, find Saksham Nagpal for more info (Group 217)
"""
__author__ = "Scaffold by Jackson Goerner, Code by Yin Lam Lo"

from poke_team import PokeTeam
from battle import Battle
from linked_list import LinkedList


def default_set():
    default = BSet(5)
    default.add(1)
    default.add(2)
    default.add(3)
    default.add(4)
    default.add(5)
    return default

class Tournament:

    def __init__(self, battle: Battle | None = None) -> None:
        """
                Constructor
                :best-case complexity:   O(1)
                :worst-case complexity:  O(1)
        """
        if battle is None:
            battle = Battle(verbosity=0)

        self.battle_sys = battle
        self.battle_mode = None
        self.team_generated = None
        self.past_battle = ArrayStack(9)
        self.flag = None
        self.flag_exception = BSet(9)

    def set_battle_mode(self, battle_mode: int) -> None:
        """
                :best-case complexity:   O(1)
                :worst-case complexity:  O(1)
        """
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool:
        """
                depend on the list length
                :best-case complexity:   O(1), n = 1
                :worst-case complexity:  O(n)
        """
        tournament_str_list = tournament_str.split()
        remaining = ArrayStack(len(tournament_str_list))
        temp = ArrayStack(len(tournament_str_list))
        for i in reversed(tournament_str_list):
            remaining.push(i)

        while len(remaining) > 0:
            temp_item = remaining.pop()
            if temp_item == '+':
                if len(temp) < 2:
                    return False
                temp.push("(" + temp.pop() + temp_item + temp.pop() + ")")
            else:
                temp.push(temp_item)

        return True

    def is_balanced_tournament(self, tournament_str: str) -> bool:
        # 1054 only
        raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        """
                        depend on the list length
                        :best-case complexity:   O(1), n = 1
                        :worst-case complexity:  O(n)
        """

        if type(tournament_str) is not str:
            raise TypeError("tournament_str must be str")
        if not self.is_valid_tournament(tournament_str):
            raise ValueError("Not a valid tournament")
        n_flag = True
        team_name_list = tournament_str.split()
        self.team_generated = LinkedList()
        for team_name in team_name_list:
            if team_name == "+":
                new_team = "+"
                if self.team_generated.__getitem__(len(self.team_generated)-1) == "+":
                    if n_flag:
                        self.flag = len(self.team_generated)+3
                        n_flag = False
            else:
                new_team = PokeTeam.random_team(team_name, self.battle_mode)
            self.team_generated.append(new_team)


    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:

        """
                        done as required
                        :best-case complexity:   O(B + P)
                        :worst-case complexity:  O(B + P)
        """

        # "Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"
        # "Roark Maylene Fantina + + Candice Volkner + +"
        # "Roark Fantina + Candice Volkner + +"
        # "Roark Candice Volkner + +"
        # "Roark Candice +"

        if len(self.team_generated) == 1:
            return None
        battle_op = self.team_generated.index("+")
        self.flag -= 3


        team1 = self.team_generated.__getitem__(battle_op - 2)
        team2 = self.team_generated.__getitem__(battle_op - 1)
        print(team1)
        print(team2)

        team1.regenerate_team() # for battle
        team2.regenerate_team()

        res = self.battle_sys.battle(team1, team2)

        if res == 1:
            self.team_generated.delete_at_index(battle_op - 1)  # delete team2 location
            self.team_generated.delete_at_index(battle_op - 1)  # delete "+"
        elif res == 2:
            self.team_generated.delete_at_index(battle_op - 2)  # delete team1 location
            self.team_generated.delete_at_index(battle_op - 1)  # delete "+"

        team1.regenerate_team()     # for meta calculation
        team2.regenerate_team()

        return team1, team2, res

    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        """
        :best-case complexity:   O(1), n = 1
        :worst-case complexity:  O(n)
        """
        l = LinkedList()
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            l.insert(0, (res[0], res[1]))
        return l

    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        """
                        done as required
                        :best-case complexity:   O(M*(B + P))
                        :worst-case complexity:  O(M*(B + P))
        """
        l = LinkedList()
        while True:
            res = self.advance_tournament()
            if res is None:
                break
            # compare that both dont have that type
            t1s = self.team_to_set(res[0].get_team_members())
            t2s = self.team_to_set(res[1].get_team_members())

            if self.flag <= 0 and len(self.past_battle) >= 2:   # if battle come from 2 diff branch, the set start merging
                temp_set = self.past_battle.pop().union(self.past_battle.pop())
                self.past_battle.push(temp_set)

            if res[2] == 1:                                     # new loser set was added
                self.past_battle.push(t2s)
            elif res[2] == 2:
                self.past_battle.push(t1s)

            if self.flag <= 0 and len(self.past_battle) >= 2:   # add the new loser into the branch set
                temp_set1 = self.past_battle.pop().union(self.past_battle.pop())
                self.past_battle.push(temp_set1)

            # default type set to compare the meta type
            meta = default_set().difference(t1s.union(t2s))

            # chk the condition of meta and turn it into str
            meta_out = []
            if len(meta) == 1 and self.flag <= 0:
                meta = str(meta).replace("{","").replace("}","")
                if meta == 1:
                    meta_out.append("FIRE")
                elif meta == 2:
                    meta_out.append("GRASS")
                elif meta == 3:
                    meta_out.append("WATER")
                elif meta == 4:
                    meta_out.append("GHOST")
                elif meta == 5:
                    meta_out.append("NORMAL")
                l.insert(0, (res[0], res[1], meta_out))
        return l

    def team_to_set(self, team: PokeTeam) -> BSet:
        """
            pokemon amount in a team
            :best-case complexity:   O(1), n = 1
            :worst-case complexity:  O(P)
        """
        set = BSet(5)
        for i in range(len(team)):
            poke = team.pop()
            if poke.get_poke_type() is PokeType.FIRE:
                set.add(1)
            elif poke.get_poke_type() is PokeType.GRASS:
                set.add(2)
            elif poke.get_poke_type() is PokeType.WATER:
                set.add(3)
            elif poke.get_poke_type() is PokeType.GHOST:
                set.add(4)
            elif poke.get_poke_type() is PokeType.NORMAL:
                set.add(5)
        return set


    def flip_tournament(self, tournament_list: LinkedList[tuple[PokeTeam, PokeTeam]], team1: PokeTeam,
                        team2: PokeTeam) -> None:
        # 1054
        raise NotImplementedError()
