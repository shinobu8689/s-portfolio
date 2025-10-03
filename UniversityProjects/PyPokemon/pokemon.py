"""
the implementation of each pokemon using PokemonBase see PokemonBase
"""
__author__ = "Scaffold by Jackson Goerner, Code by Yin Lam Lo"
"test"
from pokemon_base import PokemonBase, PokeType, Status


class Charizard(PokemonBase):
    def __init__(self, base_hp=12, poke_type=PokeType.FIRE, new_name="Charizard", base_level=3, level=3,
                 pre_damage=0, att_value=10, def_value=4, spd_value=9, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats() # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if damage > self.get_defence():
            self.lose_hp(damage * 2)
        else:
            self.lose_hp(damage)

    def update_stats(self):
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level()
        self.current_attack_value = self.base_attack_value + self.get_level() * 2
        self.current_speed_value = self.base_speed_value + self.get_level()

    def get_evolved_version(self) -> PokemonBase:
        """no evolved version"""
        return None


class Charmander(PokemonBase):
    def __init__(self, base_hp=8, poke_type=PokeType.FIRE, new_name="Charmander", base_level=1, level=1,
                 pre_damage=0, att_value=6, def_value=4, spd_value=7, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if damage > self.get_defence():
            self.lose_hp(damage)
        else:
            self.lose_hp(damage // 2)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level()
        self.current_attack_value = self.base_attack_value + self.get_level()
        self.current_speed_value = self.base_speed_value + self.get_level()

    def get_evolved_version(self) -> PokemonBase:
        """
        calculate the damage taken and return the evolved pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        diff = self.max_hp - self.current_hp
        return Charizard(level=self.get_level(), status=self.get_status(), pre_damage=diff)


class Venusaur(PokemonBase):
    def __init__(self, base_hp=20, poke_type=PokeType.GRASS, new_name="Venusaur", base_level=2, level=2,
                 pre_damage=0, att_value=5, def_value=10, spd_value=3, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if damage > self.get_defence() + 5:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage // 2)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + (self.get_level() // 2)
        self.current_speed_value = self.base_speed_value + (self.get_level() // 2)

    def get_evolved_version(self) -> PokemonBase:
        """no evolved version"""
        return None


class Bulbasaur(PokemonBase):
    def __init__(self, base_hp=12, poke_type=PokeType.GRASS, new_name="Bulbasaur", base_level=1, level=1,
                 pre_damage=0, att_value=5, def_value=5, spd_value=7, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if damage > self.get_defence() * 2:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage // 2)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level()
        self.current_speed_value = self.base_speed_value + (self.get_level() // 2)

    def get_evolved_version(self) -> PokemonBase:
        """
        calculate the damage taken and return the evolved pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        diff = self.max_hp - self.current_hp
        return Venusaur(level=self.get_level(), status=self.get_status(), pre_damage=diff)


class Blastoise(PokemonBase):
    def __init__(self, base_hp=15, poke_type=PokeType.WATER, new_name="Blastoise", base_level=3, level=3,
                 pre_damage=0, att_value=8, def_value=8, spd_value=10, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if damage > self.get_defence() * 2:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage // 2)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level() * 2
        self.current_attack_value = self.base_attack_value + (self.get_level() // 2)
        self.current_defence_value = self.base_defence_value + self.get_level()

    def get_evolved_version(self) -> PokemonBase:
        """no evolved version"""
        return None


class Squirtle(PokemonBase):
    def __init__(self, base_hp=9, poke_type=PokeType.WATER, new_name="Squirtle", base_level=1, level=1,
                 pre_damage=0, att_value=4, def_value=6, spd_value=7, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if damage > self.get_defence() * 2:
            self.lose_hp(damage)
        else:
            self.lose_hp(damage // 2)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level() * 2
        self.current_attack_value = self.base_attack_value + (self.get_level() // 2)
        self.current_defence_value = self.base_defence_value + self.get_level()

    def get_evolved_version(self) -> PokemonBase:
        """
        calculate the damage taken and return the evolved pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        diff = self.max_hp - self.current_hp
        return Blastoise(level=self.get_level(), status=self.get_status(), pre_damage=diff)


class Gengar(PokemonBase):
    def __init__(self, base_hp=12, poke_type=PokeType.GHOST, new_name="Gengar", base_level=3, level=3,
                 pre_damage=0, att_value=18, def_value=3, spd_value=12, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.lose_hp(damage)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level() // 2

    def get_evolved_version(self) -> PokemonBase:
        """no evolved version"""
        return None


class Haunter(PokemonBase):

    def __init__(self, base_hp=9, poke_type=PokeType.GHOST, new_name="Haunter", base_level=1, level=1,
                 pre_damage=0, att_value=8, def_value=6, spd_value=6, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.lose_hp(damage)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level() // 2

    def get_evolved_version(self) -> PokemonBase:
        diff = self.max_hp - self.current_hp
        return Gengar(level=self.get_level(), status=self.get_status(), pre_damage=diff)


class Gastly(PokemonBase):
    def __init__(self, base_hp=6, poke_type=PokeType.GHOST, new_name="Gastly", base_level=1, level=1,
                 pre_damage=0, att_value=4, def_value=8, spd_value=2, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.lose_hp(damage)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.max_hp = self.base_hp + self.get_level() // 2

    def get_evolved_version(self) -> PokemonBase:
        """
        calculate the damage taken and return the evolved pokemon
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        diff = self.max_hp - self.current_hp
        return Haunter(level=self.get_level(), status=self.get_status(), pre_damage=diff)


class Eevee(PokemonBase):
    def __init__(self, base_hp=10, poke_type=PokeType.NORMAL, new_name="Eevee", base_level=1, level=1,
                 pre_damage=0, att_value=6, def_value=4, spd_value=7, status=Status.NO_STATUS) -> None:
        """
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        super().__init__(base_hp, poke_type, new_name, base_level, level, pre_damage, att_value, def_value, spd_value, status)
        self.update_stats()  # update stats according to levels
        self.current_hp = self.max_hp - pre_damage  # make hp after evolved be taken the same damage as before

    def defend(self, damage: int) -> None:
        """
        determine damage compared with the defence
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        if damage >= self.get_defence():
            self.lose_hp(damage)

    def update_stats(self):
        """
        update stats after level up
        :best-case complexity:   O(1)
        :worst-case complexity:  O(1)
        """
        self.current_attack_value = self.base_attack_value + self.get_level()
        self.current_defence_value = self.base_defence_value + self.get_level()
        self.current_speed_value = self.base_speed_value + self.get_level()

    def get_evolved_version(self) -> PokemonBase:
        """no evolved version"""
        return None
