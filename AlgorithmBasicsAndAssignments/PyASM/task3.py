"""
HULK SMASH!
"""
__author__ = "Saksham Nagpal"
__date__ = "19.05.2022"

from typing import List

def smash_or_sad(the_list: List[int], hulk_power: int) -> int:
    smash_count = 0
    for i in range(len(the_list)):
        if the_list[i] <= hulk_power:
            print("Hulk SMASH! >:(")
            smash_count += 1
        else:
            print("Hulk Sad :(")
    return smash_count


def main() -> None:
    my_list = [10, 14, 16]
    hulk_power = 15
    print(f"Hulk smashed {smash_or_sad(my_list, hulk_power)} people")

main()
