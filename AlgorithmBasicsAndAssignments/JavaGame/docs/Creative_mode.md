# Requirement 4


<h1>Title:
Super Mario Bros 🔴 🟢</h1>

**Description**:
- Add a menu before the map to select the main player to be Luigi or Mario 🎮
- Both characters will have 3 lives in their stats and the game restarts every time they lose a life ❤️❤️❤️
- the game will end when player loses all lives 💔💔💔
- Luigi has the unique trait of an extra life added when he begins the game while mario only has 3 ❤️❤️❤️💔

**Explanation why it adheres to SOLID principles** (WHY):
- adheres to the Single Responsibility Principle as Luigi and Mario as two separate classes that extend the player class and each have their own responsibilities and traits when selected by the player
- Open-Close principle because both Luigi and Mario extend player and altering one will not alter the other
- Have a Lives interface that is implemented by both Mario and Luigi which adheres to Liskov Substitution principle since Luigi's special trait is more lives than mario

| Requirements                                                                                                            | Features (HOW) / Your Approach / Answer                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Must use at least two (2) classes from the engine package                                                               | Luigi's attack action will extend the Action class from the engine. He will also have his own unique capabilities from the CapabilitiesSet class.                                                                                                              |
| Must use/re-use at least one(1) existing feature (either from assignment 2 and/or fixed requirements from assignment 3) | Luigi and Mario class will be using the same classes implemented in player class like the Items package and JumpAction. Both Mario and Luigi will extend the Player class. <br/>They will both also be able to trade and collect coins as implemented before |
| Must use existing or create new abstractions (e.g., abstract or interface, apart from the engine code)                  | Both Luigi and Mario will have an abstract Lives class that will control and deal with their lives every time they are defeated                                                                                                                              |
| Must use existing or create new capabilities                                                                            | Luigi will also be using the same capabilities as the current Player class such as TALL and INVINCIBLE                                                                                                                                                       |

---

# Requirement 5

<h1>Title: 
Power ups! 👊🏻</h1>

**Description**:

- New Blind Status that limited player vision (Fog of war). Can choose on the menu for higher difficulty.
  - Any new updates on the map will show for 1 turn then it will be masked.
  - Special character will not be affected by the Blind effect
  
- More effects/status for Player and enemies for a more dynamic gameplay.
  - Effect will be capabilities which checks for every player in each turn.
  - Effects that obtain from enemies:
    1) Dizzy: Actor walks randomly for a few turns until he wakes up.
    2) Burnt: Actor takes extra damage every turn, the longer it stands on lava, the longer the effects will cool down, and more damage to the player as well.
  - Effects that randomly obtain from the 3rd fountain "Miracle Fountain" ('V'):
    1) Shield: Actor will have a shield that has 90% chance to block any damage, once attack is blocked the shield breaks.  
    2) Blessed: Actor take half damage in 5 turns. 


**Explanation why it adheres to SOLID principles** (WHY):

- Open-Close Principle: Different effects given from the water are extended from "StandardWater" so it is open to add more types of Water power ups just by extending it. And all subclass water types can benefit from the modification of the base "StandardWater" class.
- Single Responsibility Principle: Each water type are different class to only focus on its responsibility. The masking mechanism will operate inside Maskable interface itself.
- Dependency Inversion Principle: "StandardWater" is an abstract concept and its subclass are the details.
- Liskov Substitution Principle: Should be able to use any sub-water types where StandardWater is excepted.


| Requirements                                                                                                            | Features (HOW) / Your Approach / Answer                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Must use at least two (2) classes from the engine package                                                               | We will use Actor, Location, Action(MoveActorAction and DoNothingAction) from the game engine. Dizzy effects will use Class from WanderBehaviour and MoveActorAction to randomly move.        |
| Must use/re-use at least one(1) existing feature (either from assignment 2 and/or fixed requirements from assignment 3) | Shield, Blessed can obtain from drinking water (R3). Dizzy will obtain by getting hit by enemies (R2).                                                                                        |
| Must use existing or create new abstractions (e.g., abstract or interface, apart from the engine code)                  | A new Abstract Class "StandardWater" will be added as a based class for different types of special water with different effects. Maskable interface will be added for limited vision process. |
| Must use existing or create new capabilities                                                                            | New capabilities will be added: Dizzy, Burnt, Shield, Blessed                                                                                                                                 |