# Design Rationale for RQ3&4 (Enemies and Items)
## Enemies Class
Enemies are like “Goomba” are originally extended from the class “Actor”.  Enemies has different characteristics compare to ”Player”.  And we also have another enemy “Koopa”.  Instead of making another class called ”Koopa” extends from the class “Actor”, a new abstract class “Enemies” are created as the parent of “Goomba” and “Koopa”.  Because they are enemies that shared a lot of similarity.  Making “Goomba” and “Koopa” directly extend from “Actor” will repeat lots of code and violated “Don’t repeat yourself” principal.

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
    - Roomba: 20
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

## Class for Items
New classes “SuperMushroom”, “PowerStar”, and “Coin” will be created extending from parent class in engine “Item”. And “Wrench” will be extending from “WeaponItem”.  Since Item have attribute of capability, “SuperMushroom” and  “PowerStar” should store “TALL” and “STAR” capability individually.  When player consume the item from the inventory, the player should get the capability from the item and add it to player’s capability list.  The status are given from detecting capability on the player, not the player consumed item or not.

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

## Wrench
Extends from ”WeaponItems” and has Capability, with 80% hit rate and 50 damage. It gives player ability to break the shell.  Should show option to break the shell when near a shell with a wrench in the inventory.

## When Items are on the Map
When “PowerStar” is initialised on the map, an attribute in the star will count despawn time, while another item will not.  Picking up “PowerStar” or obtaining it from Toad will consume instantly, but other items can be stored in the inventory.

## Resetting the game
New method will be implemented for processing the reset:
To remove the enemies on the map, a new method in the reset class will scan through the map to see is there any enemies class exist on the map and remove all of them.
Player status will reset by new method in Player class, the CapabilityList will be emptied, counter for mushroomEaten will reset to 0 as well.
Healing the player by running the Actor.resetMaxHp(100 + 50 * mushroomEaten), since mushroomEaten will reset to 0, this should set it to the default state
Detecting the Class Coin on the map the same as checking enemies, and remove them from the map.



