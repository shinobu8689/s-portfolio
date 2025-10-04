# Design Rationale for Reqs 1, 2, and 7

## Trees
### Tree
The tree class will be abstract. Each type of tree will be its own class, a child of the tree class. The actions specific to these types will be implemented in these child classes. 
- Contains a age attribute
- Every 10 ticks of age, changes the object to the next type of tree. This will be overridden in the mature tree
- Has a 50% chance to delete the tree object and change the ground to dirt. (For reseting the game)

### Sprout (+)
- 10% chance to instantiate a Goomba object on the location if there is no other actor on the location, without affecting the tree object.

### Sapling (t)
- 10% chance to instantiate a $20 coin object on the location, without affecting the tree object.

### Mature (T)
- 15% chance to spawn Koopa object on the location if no other actor is on the location, without affecting tree object.  
- Every 5 ticks past growing to be mature, will attempt to instantiate new sprout object on adjacent dirt. If no dirt is available, nothing will happen.  
- 20% chance to delete the tree object and change location state back to dirt.
---

## Jumping
The JumpAction class will handle the player jump. This will contain the probability of success for each ground type, as well as the fall damage if the player does not succeed. It will also contain the method to carry out the jump action, as well as to then either move or hurt the player. The class will also check if the player has the SuperMushroom super jump capability and will act accordingly if the player does have this. 

---

## Reset game

The reset game action class will call functions in the tree class, the enemy class, the player class and the coin class that will then delete those objects (in the case of the trees, the enemies and the coins), and change the player's health and status back to the default. These functions will be implemented in their designated classes as there is a bit of logic to deal with. In particular, the only half of the trees will be deleted, and this is handled by the tree class. Therefore instead of putting the reset functionality in this class, it will just call the methods in other objects.
