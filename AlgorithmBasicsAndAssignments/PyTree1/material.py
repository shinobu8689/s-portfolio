from random_gen import RandomGen

# Material names taken from https://minecraft-archive.fandom.com/wiki/Items
RANDOM_MATERIAL_NAMES = [
    "Arrow",
    "Axe",
    "Bow",
    "Bucket",
    "Carrot on a Stick",
    "Clock",
    "Compass",
    "Crossbow",
    "Exploration Map",
    "Fire Charge",
    "Fishing Rod",
    "Flint and Steel",
    "Glass Bottle",
    "Dragon's Breath",
    "Hoe",
    "Lead",
    "Map",
    "Pickaxe",
    "Shears",
    "Shield",
    "Shovel",
    "Sword",
    "Saddle",
    "Spyglass",
    "Totem of Undying",
    "Blaze Powder",
    "Blaze Rod",
    "Bone",
    "Bone meal",
    "Book",
    "Book and Quill",
    "Enchanted Book",
    "Bowl",
    "Brick",
    "Clay",
    "Coal",
    "Charcoal",
    "Cocoa Beans",
    "Copper Ingot",
    "Diamond",
    "Dyes",
    "Ender Pearl",
    "Eye of Ender",
    "Feather",
    "Spider Eye",
    "Fermented Spider Eye",
    "Flint",
    "Ghast Tear",
    "Glistering Melon",
    "Glowstone Dust",
    "Gold Ingot",
    "Gold Nugget",
    "Gunpowder",
    "Ink Sac",
    "Iron Ingot",
    "Iron Nugget",
    "Lapis Lazuli",
    "Leather",
    "Magma Cream",
    "Music Disc",
    "Name Tag",
    "Nether Bricks",
    "Paper",
    "Popped Chorus Fruit",
    "Prismarine Crystal",
    "Prismarine Shard",
    "Rabbit's Foot",
    "Rabbit Hide",
    "Redstone",
    "Seeds",
    "Beetroot Seeds",
    "Nether Wart Seeds",
    "Pumpkin Seeds",
    "Wheat Seeds",
    "Slimeball",
    "Snowball",
    "Spawn Egg",
    "Stick",
    "String",
    "Wheat",
    "Netherite Ingot",
]

class Material:

    def __init__(self, name: str, mining_rate: float) -> None:
        '''
            Initialises a material
            Parameters: name (str), mining_rate (float)
            Return:     None
            Complexity: O(1)
        '''
        self.name = name
        self.mining_rate = mining_rate
    
    def __str__(self) -> str:
        '''
            to_string method
            Complexity: O(1)
        '''
        return f"{self.name}: {self.mining_rate}🍗/💎"

    @classmethod
    def random_material(cls):
        '''
            Generate a random material based on the provided name list
            with the material list given
            Parameters: material_list (list[Material])
            Return:     Material object
            Complexity: O(1)
        '''
        new_name = RANDOM_MATERIAL_NAMES[RandomGen.randint(0, len(RANDOM_MATERIAL_NAMES) - 1)]
        new_mining_rate = RandomGen.randint(1, 128)
        return cls(new_name, new_mining_rate)

if __name__ == "__main__":
    print(Material("Coal", 4.5))
    for n in range(5):
        print(Material.random_material())

