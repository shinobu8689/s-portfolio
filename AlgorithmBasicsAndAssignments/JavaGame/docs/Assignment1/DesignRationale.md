# Design Rationale

## Requirement 1

### Tree Class
The tree class will be abstract. Each type of tree will be its own class, a child of the tree class. The actions specific to these types will be implemented in these child classes in order to keep to SOLID principles. 
In addition, the tree class extends JumpableGround class, which is new, instead of the Ground class from the engine. This will be discussed in req2. The tree class also contains some shared code between all types of trees, in order to comply with DRY principles. 
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

## Requirement 2
### Jump Class
The JumpAction class will handle the player jump. This will contain the probability of success for each ground type, as well as the fall damage if the player does not succeed. It will also contain the method to carry out the jump action, as well as to then either move or hurt the player. The class will also check if the player has the SuperMushroom super jump capability and will act accordingly if the player does have this. In addition, any type of ground that can be jumped onto will extend the JumpableGround class instead of the Ground class. This class is an extension of Ground, with some added code and attributes that are shared between all jumpable ground types. This is used in order to comply with DRY principles. 

---

## Requirement 3
### Enemies Class
Enemies are like “Goomba” are originally extended from the class “Actor”.  Enemies have different characteristics compare to ”Player”.  And we also have another enemy “Koopa”.  Instead of making another class called ”Koopa” extends from the class “Actor”, a new abstract class “Enemies” are created as the parent of “Goomba” and “Koopa”.  Because they are enemies that shared a lot of similarity.  Making “Goomba” and “Koopa” directly extend from “Actor” will repeat lots of code and violated “Don’t repeat yourself” principal.
By creating a new abstract class Enemy, it will achieve Open/closed principle.  If we want to add a new enemy, we just have to create a new enemy class that extends from Enemy.  But the core of the enemies behaviour is inside the Enemy Class, if we want to add new functionality, we could do it the Enemy Class and every enemy could have the same method from their parent class.

<br /> The “Enemies” class groups the common point of “Goomba” and “Koopa”:

- Shared Attribute: hp, damage, hitRate, disappearRate, displayChar
- Enemy cannot walk through the ground type “Floor”
- Spawn from the ground type “Tree”
    - GameMap.addActor(Actor actor, Location location)
- If the target attacks them, or within their radius
    - Enemy should start following the target and attack if within range
    - this.behaviours.put(priority, new AttackBehaviour());
    - Actor.getIntrinsicWeapon()
- Else
    - Enemy will wander around until they were killed/removed
    - this.behaviours.put(priority, new WanderBehaviour());

<br /> Different value and condition for implementing “Goomba” and “Koopa”:

- Spawn Condtion:
    - Goomba: 10% from ground type “Tree” in Sprouts state
    - Koopa: 15% from ground type “Tree” in Mature state
- HP:
    - Goomba: 20
    - Koopa: 100
- Attack Damage:
    - Goomba: 10
    - Koopa: 30
- Hit Rate:
    - Both: 50% (Default)
- Condition to get remove from the map:
    - Goomba: HP <= 0
    - Koopa: Get hit by wrench in dormant state
- Item drop when killed:
    - Goomba: None
    - Koopa: SuperMushroom
- Dormant state (Koopa only):
    - When HP <= 0, stay on the ground cannot attack nor move)

---

## Requirement 4
### Items Class
New classes “SuperMushroom”, “PowerStar”, and “Coin” will be created extending from parent class in engine “Item”. And “Wrench” will be extending from “WeaponItem”.  Since Item have attribute of capability, “SuperMushroom” and  “PowerStar” should store “TALL” and “STAR” capability individually.  When player consume the item from the inventory, the player should get the capability from the item and add it to player’s capability list.  The status are given from detecting capability on the player, not the player consumed item or not.
All the capability changes for player will be processed inside the Player class, to achieve single responsibility principle for managing the changes of the players.
And ConsumeItemAction is managing which methods to call for corresponding capability methods

<br /> New attribute should be added to “Player”:

- Integer mushroomEaten; ( to determine maximum health )
- Integer starTimer; ( to keep track the star effect duration )

<br /> When Player consumed ”SuperMushroom”:

- Player get “TALL” status in its capabilitiesSet
    - Player.addCapabilityList(“TALL”)
- Change the display character to “M”
    - Actor.setDisplayChar(“M”)
- Depends on R2: JumpAction Class
    - override all jumpRate = 100%
    - override all fallDamage = 0
- Increase Max HP + Heal
    - Count how many mushrooms eaten: mushroomEaten++
    - Set the max HP: Actor.resetMaxHp(100 + 50 * mushroomEaten)

<br /> When Player got damaged:

- Remove tall status from player’s capabilitiesSet
    - Player.removeCapabilityList(“TALL”)
- Change the display character to “m”
    - Actor.setDisplayChar(“m”)
- Remove jumpRate and fallDamage override
- Keep Max HP (Nothing to implement)

<br /> When Player consume “PowerStar”:

- Player get “STAR” status in its capabilitiesSet
    - Player.addCapabilityList(“STAR”)
- Start starTimer countdown for 10 turns
    - starTimer++
- Makes player hittable with 0 damage
    - Disable hurt() execute using if
- R2: Bypass jump action
- Set ground to dirt when the ground is Wall/Tree
    - Location.setground(Dirt)
    - Location.addItem(Coin)
- Kill attack target if hit

<br /> When starTimer == 0:

- Disable abilities the star given

### Wrench Class
Extends from ”WeaponItems” and has Capability, with 80% hit rate and 50 damage. It gives player ability to break the shell.  Should show option to break the shell when near a shell with a wrench in the inventory.

#### When Items are on the Map
When “PowerStar” is initialised on the map, an attribute in the star will count despawn time, while another item will not.  Picking up “PowerStar” or obtaining it from Toad will consume instantly, but other items can be stored in the inventory.

For ConsumerItemAction, it will check the class of the instance to ensure which type of item is it and call the correct method in player to add different capabilities. 

---
## Requirement 5
### Toad Class
Toad class is responsible for creating a new object of the monologue action in order to interact with the player.
Player will execute an interaction with toad to which he will execute to the monologue class and output a string on the console.

Relevant methods used by Toad:
- execute(actor, map): Toad will perform the action of Monologue


### Monologue Action Class
Monologue class extends the abstract Action class. It has a dependency on the Player, Utils and Wrench classes. Monologue does most of the work in terms of outputting and calling methods to create the sentences that Toad is to speak.

Relevant methods used by Monologue:
- getWeapon() from Player: will return the item as a weapon. This checks if the item that is returned.
- hasCapabilites(): checks if the capability of the player is of PowerStar. This returns a boolean of if the capability exists on the Player.
- Utilis.getNum(): this will call the static class Utils and have it generate a random number from 1-4 which will be returned.

Monologue will proceed to check the weapon in hand and power star active in order to check if the number generated by Utils is subitable to print. If not, it will ask Utils to regenerate.
Monologue will then print to toad the relevant string in which Toad will output.


### Wrench, PowerStar and Player
These classes exist primarily to use their methods for Monologue class.
<br /> Player is called by Monologue to check for its getWeapons() hence dependency. Player also has PowerStar and Wrench as it's attributes.
<br /> Power Star and Wrench both extend the abstract items class, since they are an Item held by the Player.


### Utils Class
Its primary objective is to return an int from 1-4 for Monologue to randomly output a String.

Relevant methods in Utils:
- getNum(): returns a int of 1 to 4

---

## Requirement 6
### Toad Class
Toads primary purpose is to be able to interact with the player. Once the player interacts with toad, it will create a new Trade Action object and display the menu of possible trade options the player has.
The player then selects the trade option needed and passes to Toad which will directly use the Trade Class to process this.

Relevant methods used by Toad:
- create new Trade object
- execute(actor, map): executes the selection to the trade class
- playTurn(): shows selection made by player
- menuDescription(): shows the player all the selections.


### Trade Class
Trade class is responsible for taking in the selection made by the player through Toad and execute the relevant actions. It is extended from the Actions class and is dependent on the PlayerInventory, Wallet, SuperMushroom, PowerStar, and Wrench class.
Trade class will call the getWallet() to show the amount available for trade. It will then subtract the relevant amount from the wallet int for the trade selected by the player. If the wallet < 0, Trade class will output an error message to Toad to display on the menu. If wallet > 0 then trade class will deduce the amount and update the wallet class.
It will then call player inventory and create a new instance of the Item that the player wants, then append into the PlayerInventory. Once transaction complete, it will output a sucess message to Toad to display on the menu.

Relevant methods used by Trade:
- Wallet: getWalletAmount(): shows trade how much money is current in the wallet
- Wallet: removeAmount(): remove the amount of the item from wallet
- creates new instance of SuperMushroom, Wrench or PowerStar
- TransactError(): outputs an error message due to wallet
- SuccessMessage(): outputs a success message
- Player: addItemToInventory(): allows to append the item bought into the PlayerInventory


### Player Inventory Class
Player Inventory class is extended from the Actor class which allows it to use the GetInventory() and RemoveInventory() methods.
It also has a dependency on the items class to get the ticks() method as some requirements indicate the PowerStar object will disappear from the inventory.

Relevant methods used by PlayerInventory:
- Ticks(): allows to remove the PowerStar after a certain amount of ticks.


### Wallet Class
Wallet class's primary goal is to keep track of the amount of coins collected by the player. It will store this in itself as an integer and be able to have a setter which changes the amount depending on Trade Class's use and a getter to show the amount present in the class.
Trade class is hence dependent on Wallet Class.

Relevant methods in Wallet:
- GetAmount(): shows the amount of money in the wallet
- removeAmount(): take money away from the wallet due to trade


### Wrench, PowerStar and Mushroom Classes
Wrench, Power Star and SuperMushroom class have the interface of ItemPrice. This allows each item to have an int price, so that when called by the Trade Class (dependancy) for its getPrice() method it will return a price for the Trade Class to use.

Relevant methods in Wrench Power and SuperMushroom Class:
- getPrice(): shows the price of the relevant item called

---

## Requirement 7
### Resetting the game
Resettable will be implemented for processing the reset:
To remove the enemies on the map, a method from resettable will reset the registered instance, any enemies class exist on the map and remove all of them.
In the class that implemented Resettable, it will call by the run method in ResetManager which each class should have their own reset code with will not interrupt other class, which achieved single responsibility principle.