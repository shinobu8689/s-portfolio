"""
the implementation of the battle
"""
__author__ = "Scaffold by Jackson Goerner, Code by Yin Lam Lo"

from random_gen import RandomGen
from poke_team import Action, PokeTeam, Criterion
from print_screen import print_game_screen

class Battle:
    
    def __init__(self, verbosity=0) -> None:
        """
        no attribute needed for the battle field
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        pass

    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        """
        where the battle happened
        :best-case complexity:   O(n)   each loop is each round, it depends on the pokemon strength
        :worst-case complexity:  O(n)
        """

        # get the first pokemon
        team1_poke = team1.retrieve_pokemon()
        team2_poke = team2.retrieve_pokemon()

        turn = 0
        while True:
            turn += 1
            print("Turn:", turn)
            print(team1, " : ", team1_poke, team1_poke.get_status())
            print(team2, " : ", team2_poke, team2_poke.get_status())

            # get the action for both opponent
            action1 = team1.choose_battle_option(team1_poke, team2_poke)
            action2 = team2.choose_battle_option(team2_poke, team1_poke)
            if action1 == 0:
                print(team1.get_team_name(), " healed for 3 times make him lose the game.")
                return 2
            if action2 == 0:
                print(team2.get_team_name(), " healed for 3 times make him lose the game.")
                return 1


            # operate their action
            # Handle any swap actions
            if action1 is Action.SWAP:
                team1_poke = self.swap_action(team1, team1_poke)
            if action2 is Action.SWAP:
                team2_poke = self.swap_action(team2, team2_poke)

            # Handle any special actions
            if action1 is Action.SPECIAL:
                team1_poke = self.special_action(team1, team1_poke)
            if action2 is Action.SPECIAL:
                team2_poke = self.special_action(team2, team2_poke)

            # Handle any heal actions
            if action1 is Action.HEAL:
                self.heal_action(team1, team1_poke)
            if action2 is Action.HEAL:
                self.heal_action(team2, team2_poke)

            # Handle attacks
            if team1_poke.get_speed() == team2_poke.get_speed():
                if action1 is Action.ATTACK:
                    self.attack_action(team1_poke, team2_poke)
                if action2 is Action.ATTACK:
                    self.attack_action(team2_poke, team1_poke)
            elif team1_poke.get_speed() >= team2_poke.get_speed():      # when at different spd the defencing pokemon fainted wont attack after
                if action1 is Action.ATTACK:
                    self.attack_action(team1_poke, team2_poke)
                if action2 is Action.ATTACK and not team2_poke.is_fainted():
                    self.attack_action(team2_poke, team1_poke)
            elif team1_poke.get_speed() < team2_poke.get_speed():
                if action2 is Action.ATTACK:
                    self.attack_action(team2_poke, team1_poke)
                if action1 is Action.ATTACK and not team1_poke.is_fainted():
                    self.attack_action(team1_poke, team2_poke)

            # If both pokemon are still alive, then they both lose 1 HP
            if not team1_poke.is_fainted() and not team2_poke.is_fainted():
                team1_poke.lose_hp(1)
                team2_poke.lose_hp(1)

            # If one pokemon has fainted and the other has not, the remaining pokemon level up
            if not team1_poke.is_fainted() and team2_poke.is_fainted():
                team1_poke.level_up()
            if team1_poke.is_fainted() and not team2_poke.is_fainted():
                team2_poke.level_up()

            # If pokemon have not fainted and can evolve, they evolve
            if team1_poke.can_evolve():
                team1_poke = team1_poke.get_evolved_version()
            if team2_poke.can_evolve():
                team2_poke = team2_poke.get_evolved_version()

            # Fainted pokemon are returned and a new pokemon is retrieved from the team.
            if team1_poke.is_fainted():
                if team1.is_empty():
                    team2.return_pokemon(team2_poke)
                    break
                team1_poke = team1.retrieve_pokemon()
            if team2_poke.is_fainted():
                if team2.is_empty():
                    team1.return_pokemon(team1_poke)
                    break
                team2_poke = team2.retrieve_pokemon()


            ("============")

        print()
        print(" >>> ====== RESULT ====== <<< ")
        print(team1)
        print(team2)


        # return the result

        if team1.is_empty():
            print(2)
            print(" >>> ======   END   ====== <<< ")
            print()
            return 2
        elif team2.is_empty():
            print(1)
            print(" >>> ======   END   ====== <<< ")
            print()
            return 1
        else:
            return 0

    def attack_action(self, offence_poke, defence_poke):
        """
        do the attack and print a str
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        damage = str(offence_poke.attack(defence_poke))
        print(offence_poke, "attacks ", defence_poke, ". Result:", offence_poke, defence_poke)

    def swap_action(self, offence_team, offence_poke):
        """
        swap the pokemon and print a str
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        offence_team.return_pokemon(offence_poke)
        new_poke = offence_team.retrieve_pokemon()
        print(offence_team.get_team_name(), "swapped out", offence_poke, "and got", new_poke )
        return new_poke

    def special_action(self, offence_team, offence_poke):
        """
        do the special and print a str
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        offence_team.return_pokemon(offence_poke)
        offence_team.special()
        new_poke = offence_team.retrieve_pokemon()
        print(offence_team.get_team_name(), "used special with", offence_poke, "and got", new_poke)
        return new_poke

    def heal_action(self, offence_team, offence_poke):
        """
        do the heal and print a str
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        offence_team.heal_action(offence_poke)
        print(offence_team.get_team_name(), "healed", offence_poke)
