from poke_team import Action, Criterion, PokeTeam
from random_gen import RandomGen
from pokemon import Bulbasaur, Charizard, Charmander, Gastly, Squirtle, Eevee
from tests.base_test import BaseTest
from battle import Battle
from tournament import Tournament
from tower import BattleTower


class UnitTestPokeTeam(BaseTest):

    # no test for random test since it how random_gen mechanism is a serect
    # so we do not know what the one generated should look like

    # unit test for __init__

    def test_init_1(self):
        t = PokeTeam("init1", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        # C B S G E
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Charmander, Bulbasaur, Squirtle, Gastly, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_init_2(self):
        t = PokeTeam("sbm1", [0, 0, 0, 2, 3], 1, PokeTeam.AI.ALWAYS_ATTACK, Criterion.HP)
        # G G E E E
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Gastly, Gastly, Eevee, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_init_3(self):
        t = PokeTeam("sbm2", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.HP)
        # B S E C G
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Bulbasaur, Squirtle, Eevee, Charmander, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)


    # unit test for return_pokemon

    def test_return_pokemon_bm0(self):
        t = PokeTeam("rtn_bm0", [1, 1, 1, 0, 2], 0, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Charmander, Charmander, Charmander, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_return_pokemon_bm1(self):
        t = PokeTeam("rtn_bm1", [0, 0, 1, 3, 1], 1, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Gastly, Gastly, Gastly, Eevee, Squirtle]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_return_pokemon_bm2(self):
        t = PokeTeam("rtn_bm2", [0, 1, 1, 2, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.SPD)
        p = t.retrieve_pokemon()
        t.return_pokemon(p)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Eevee, Bulbasaur, Squirtle, Gastly, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)


    # unit test for retrieve_pokemon

    def test_retrieve_pokemon_1(self):
        t = PokeTeam("rte1", [2, 2, 2, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Charmander, Charmander, Bulbasaur, Bulbasaur, Squirtle, Squirtle]
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_retrieve_pokemon_2(self):
        t = PokeTeam("rte2", [3, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Charmander, Charmander, Charmander]
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_retrieve_pokemon_3(self):
        t = PokeTeam("rte3", [1, 0, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Charmander, Squirtle, Gastly, Eevee]
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)


    # unit test for special action

    def test_special_mode_0(self):
        t = PokeTeam("sbm0", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        # C B S G E
        t.special()
        # E B S G C
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Eevee, Bulbasaur, Squirtle, Gastly, Charmander]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_special_mode_1(self):
        t = PokeTeam("sbm1", [0, 0, 0, 2, 3], 1, PokeTeam.AI.ALWAYS_ATTACK, Criterion.HP)
        # G G E E E
        t.special()
        # E E E G G
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Eevee, Eevee, Eevee, Gastly, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_special_mode_2(self):
        t = PokeTeam("sbm2", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.HP)
        # B S E C G
        t.special()
        # G C E S B
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Gastly, Charmander, Eevee, Squirtle, Bulbasaur]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    # unit test for PokeTeam regenerate_team

    def test_regenerate_team_1(self):
        t = PokeTeam("t1", [3, 2, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        # This should end, since all pokemon are fainted, slowly.
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Charmander, Charmander, Charmander, Bulbasaur, Bulbasaur]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_regenerate_team_2(self):
        t = PokeTeam("t2", [0, 0, 0, 4, 2], 0, PokeTeam.AI.ALWAYS_ATTACK)
        # This should end, since all pokemon are fainted, slowly.
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Gastly, Gastly, Gastly, Gastly, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_regenerate_team_3(self):
        t = PokeTeam("t3", [0, 0, 2, 2, 2], 0, PokeTeam.AI.ALWAYS_ATTACK)
        # This should end, since all pokemon are fainted, slowly.
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Squirtle, Gastly, Gastly, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)


    # unit test for PokeTeam is_empty

    def test_is_empty_1(self):
        t = PokeTeam("t1", [0, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        self.assertEqual(t.is_empty(), True)

    def test_is_empty_2(self):
        t = PokeTeam("t2", [1, 1, 1, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        t.retrieve_pokemon()
        t.retrieve_pokemon()
        t.retrieve_pokemon()
        self.assertEqual(t.is_empty(), True)

    def test_is_empty_3(self):
        t = PokeTeam("t3", [0, 0, 0, 1, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon()
        self.assertEqual(t.is_empty(), True)


    # unit test for PokeTeam choose battle option

    def test_battle_option_swap_1(self):  # test swap action
        t = PokeTeam("option1", [1, 1, 1, 0, 0], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        p = t.retrieve_pokemon()
        e = Squirtle()
        self.assertEqual(t.choose_battle_option(p, e), Action.SWAP)

    def test_battle_option_swap_2(self):  # test swap action
        t = PokeTeam("option2", [0, 1, 1, 0, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        p = t.retrieve_pokemon()
        e = Charmander()
        self.assertEqual(t.choose_battle_option(p, e), Action.SWAP)

    def test_battle_option_swap_3(self):  # test swap action
        t = PokeTeam("option3", [0, 0, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        p = t.retrieve_pokemon()
        e = Bulbasaur()
        self.assertEqual(t.choose_battle_option(p, e), Action.SWAP)


    # 3 unit test fpr PokeTeam __str__

    def test_string_bm0(self):  # test did it followed pokedex order
        t = PokeTeam("bm0", [1, 1, 1, 1, 1], 0, PokeTeam.AI.RANDOM)
        self.assertEqual(str(t), "bm0 (0): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")

    def test_string_bm2(self):  # test when Bulbasaur & Squirtle in the same team with same Speed
        t = PokeTeam("bm2", [1, 1, 2, 1, 0], 2, PokeTeam.AI.RANDOM, Criterion.SPD)
        self.assertEqual(str(t), "bm2 (2): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP]")

    def test_string_bm2_pkd(self):  # test when they are all the same level, shld be in pokedex order
        t = PokeTeam("bm2", [1, 1, 1, 1, 1], 2, PokeTeam.AI.RANDOM, Criterion.LV)
        self.assertEqual(str(t), "bm2 (2): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")


class UnitTestBattle(BaseTest):

    # Unit test for battle

    def test_battle_1(self):
        RandomGen.set_seed(192837465)
        team1 = PokeTeam("Person A", [1, 2, 1, 0, 0], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.HP)
        team2 = PokeTeam("Person B", [0, 0, 0, 2, 2], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 9)
        self.assertIsInstance(remaining[0], Charmander)
        self.assertEqual(remaining[1].get_hp(), 8)
        self.assertIsInstance(remaining[1], Squirtle)

    def test_battle_2(self):
        RandomGen.set_seed(16620015)
        team1 = PokeTeam("Person A", [0, 2, 1, 1, 1], 0, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        team2 = PokeTeam("Person B", [0, 2, 0, 2, 2], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].get_hp(), 10)
        self.assertIsInstance(remaining[0], Eevee)

    def test_battle_3(self):
        RandomGen.set_seed(1992560)
        team1 = PokeTeam("Person A", [0, 2, 1, 2, 1], 1, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Person B", [1, 2, 0, 1, 2], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.SPD)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].get_hp(), 1)
        self.assertIsInstance(remaining[0], Eevee)


    # unit test for BattleTower, __init__, set_my_team, and generate_teams
    # they need to work together to test

    def test_tower_init_1(self):
        RandomGen.set_seed(3533)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("E", 1, team_size=6, criterion=Criterion.SPD))
        bt.generate_teams(5)
        RandomGen.set_seed(1032873918273)
        results = [
            (1, 5),
            (1, 8),
            (1, 5),
            (1, 4),
            (2, 4)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)

    def test_tower_init_2(self):
        RandomGen.set_seed(44444)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("G", 1, team_size=6))
        bt.generate_teams(4)
        RandomGen.set_seed(156453343)
        results = [
            (1, 9),
            (2, 6)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)

    def test_tower_init_3(self):
        RandomGen.set_seed(55555)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Q", 0, team_size=5))
        bt.generate_teams(3)
        RandomGen.set_seed(8224443)
        results = [
            (1, 6),
            (2, 2)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)


    # unit test for __next__

    def test_next_1(self):
        RandomGen.set_seed(244443)

        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("U", 0, team_size=6))
        bt.generate_teams(4)

        it = iter(bt)

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))

        self.assertEqual(l, [
            (1, 2),
            (1, 9),
            (1, 7),
            (2, 4)
        ])

    def test_next_2(self):
        RandomGen.set_seed(24323)

        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("X", 0, team_size=5))
        bt.generate_teams(2)

        it = iter(bt)

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))

        self.assertEqual(l, [
            (1, 5),
            (1, 6),
            (2, 5)
        ])

    def test_next_3(self):
        RandomGen.set_seed(24323)

        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("R", 0, team_size=4))
        bt.generate_teams(1)

        it = iter(bt)

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))

        self.assertEqual(l, [
            (1, 5),
            (1, 4),
            (2, 4)
        ])


    # unit test for avoid_duplicates

    def test_dup_1(self):
        RandomGen.set_seed(324)

        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("U", 0, team_size=6))
        bt.generate_teams(4)

        it = iter(bt)
        it.avoid_duplicates()
        # removed 2 teams

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))

        self.assertEqual(l, [
            (1, 5),
            (2, 8)
        ])

    def test_dup_2(self):
        RandomGen.set_seed(243333)

        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("X", 0, team_size=5))
        bt.generate_teams(7)

        it = iter(bt)
        it.avoid_duplicates()
        # removed 6 teams

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))

        self.assertEqual(l, [
            (1, 9),
            (2, 9)
        ])

    def test_next_3(self):
        RandomGen.set_seed(24323)

        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("R", 0, team_size=4))
        bt.generate_teams(6)

        it = iter(bt)
        it.avoid_duplicates()
        # removed 5 team

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))

        self.assertEqual(l, [
            (1, 3),
            (2, 3)
        ])


    # unit test for task 6

    # unit test for __init__, set_battle_mode, is_valid_tournament
    # we test them together because they rely on each other

    def test_prepare_tournament_team_1(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("A B + C D + + + E F + G H + +"))
        t.start_tournament("A B + C D + + E F + G H + + +")

    def test_prepare_tournament_team_2(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("A B + +  C D + E F + + G H + + + "))
        t.start_tournament("A B + C D + E F + + G H + + + ")

    def test_prepare_tournament_team_3(self):
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("A B + +  C D + E F + + + + "))
        t.start_tournament("A B + C D + E F + + +")

    # unit test for advance tournament

    def test_adv_1(self):
        RandomGen.set_seed(2123578)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("A B + C D + + E F + G H + + +")

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("A"))
        self.assertTrue(str(team2).startswith("B"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("C"))
        self.assertTrue(str(team2).startswith("D"))


    def test_adv_2(self):
        RandomGen.set_seed(210455478)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("A B + C D + E F + + G H + + + ")

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("A"))
        self.assertTrue(str(team2).startswith("B"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("C"))
        self.assertTrue(str(team2).startswith("D"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("E"))
        self.assertTrue(str(team2).startswith("F"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("C"))
        self.assertTrue(str(team2).startswith("E"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("G"))
        self.assertTrue(str(team2).startswith("H"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("C"))
        self.assertTrue(str(team2).startswith("G"))

    def test_adv_3(self):
        RandomGen.set_seed(2153478)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("A B + C D + E F + + +")

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("A"))
        self.assertTrue(str(team2).startswith("B"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("C"))
        self.assertTrue(str(team2).startswith("D"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("E"))
        self.assertTrue(str(team2).startswith("F"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("C"))
        self.assertTrue(str(team2).startswith("E"))

        team1, team2, res = t.advance_tournament()
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("G"))
        self.assertTrue(str(team2).startswith("H"))


    # unit test for linked_list_with_metas

    def test_metas_1(self):
        RandomGen.set_seed(210455478)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("A B + C D + E F + + G H + + + ")
        l = t.linked_list_with_metas()

        expected = [
            [],
            [],
            ['FIRE'],
            ['GRASS'],
            [],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

    def test_metas_2(self):
        RandomGen.set_seed(2123578)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("A B + C D + + E F + G H + + +")
        l = t.linked_list_with_metas()

        expected = [
            [],
            [],
            [],
            ['WATER'],
            ['FIRE'],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

    def test_metas_1(self):
        RandomGen.set_seed(2153478)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("A B + C D + E F + + +")
        l = t.linked_list_with_metas()

        expected = [
            [],
            ['GRASS'],
            [],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)