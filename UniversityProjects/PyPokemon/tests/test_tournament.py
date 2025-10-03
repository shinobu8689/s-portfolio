from random_gen import RandomGen
from tournament import Tournament
from battle import Battle
from tests.base_test import BaseTest


"""
Code of task 6 are incomplete, only partially done, due to non-active teammates
group grief form was submitted, find Saksham Nagpal for more info (Group 217)
"""

class TestTournament(BaseTest):

    def test_creation(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + + + Fantina Byron + Candice Volkner + + +"))
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

    def test_random(self):
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

        team1, team2, res = t.advance_tournament() # Roark vs Gardenia
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Gardenia"))

        team1, team2, res = t.advance_tournament() # Maylene vs Crasher_Wake
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Crasher_Wake"))

        team1, team2, res = t.advance_tournament() # Fantina vs Byron
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Fantina"))
        self.assertTrue(str(team2).startswith("Byron"))

        team1, team2, res = t.advance_tournament() # Maylene vs Fantina
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Roark vs Fantina
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Candice vs Volkner
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Candice"))
        self.assertTrue(str(team2).startswith("Volkner"))

        team1, team2, res = t.advance_tournament() # Roark vs Candice
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Candice"))

    def test_metas(self):
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")
        l = t.linked_list_with_metas()
        # Roark         = [0, 2, 1, 1, 1]   {2,3,4,5}
        # Garderia      = [0, 0, 2, 0, 1]   {3,5}
        # Maylene       = [6, 0, 0, 0, 0]   {1}
        # Crasher_Wake  = [0, 2, 0, 1, 0]   {2,4}
        # Fantina       = [0, 0, 1, 1, 1]   {3,4,5}
        # Byron         = [0, 2, 0, 0, 1]   {2,5}
        # Candice       = [2, 2, 1, 0, 0]   {1,2,3}
        # Volkner       = [0, 5, 0, 0, 0]   {2}

        # "Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"
        # "Roark Maylene Fantina + + Candice Volkner + +"
        # "Roark Fantina + Candice Volkner + +"
        # "Roark Candice Volkner + +"
        # "Roark Candice +"

        # "Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + & + Candice Volkner + +"

        expected = [
            [],         # Roark Candice
            [],         # Candice Volkner {4, 5}
            ['FIRE'],   # Roark Fantina {1} do not have Fire types, but Maylene (one in the loser team has it) does (lost to Fantina)
            ['GRASS'],  # Maylene Fantina {2} do not have Grass types, but Byron/Crasher_Wake (one in the loser team has it) does (lost to Fantina/Maylene)
            [],         # Fantina Byron {1}
            [],         # Maylene Crasher_Wake {3, 5}
            [],         # Roark Gardenia {1}
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

    def test_balance(self):
        # 1054
        t = Tournament()
        self.assertFalse(t.is_balanced_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"))
