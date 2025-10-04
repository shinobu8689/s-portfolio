package game.enemies;

import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.Resettable;
import game.Status;
import game.WeaponEffect;
import game.behaviour.AggressiveBehaviour;
import edu.monash.fit2099.engine.actors.Actor;
import game.items.PeachKey;

public class Bowser extends Enemy {
    private Location bowserSpawnPoint;
    /**
     * A class representing the final boss of the game, Bowser.
     */
    public Bowser() {
        super("Bowser", 'B', 500);
        this.behaviours.put(2, new AggressiveBehaviour());
        this.addCapability(WeaponEffect.FLAMETHROWER); // Adds the flamethrower to his arsenal
        this.addItemToInventory(new PeachKey()); // He drops this when he dies, so the player can free Peach

        this.addCapability(Status.FINAL_BOSS); // He is the FINAL BOSS
        registerInstance();
    }

    // when the mario loses a life and chooses to replay the game, Bowser goes back
    // to his original spot guarding the gates
    public Location getBowserSpawnPoint() {
        return bowserSpawnPoint;
    }

    public void setBowserSpawnPoint(Location bowserSpawnPoint) {
        this.bowserSpawnPoint = bowserSpawnPoint;
    }

    @Override
    protected IntrinsicWeapon getIntrinsicWeapon() {
        return new IntrinsicWeapon(80 + 15 * powerGauge, "punches");
    }

    @Override
    /**
     * Resetting the game returns Bowser to his original spawn point, and heals him to max.
     */
    public void resetInstance(Actor actor, GameMap map) {
        this.behaviours.clear();
        this.healMaximum();
        if(!(getBowserSpawnPoint().containsAnActor())) {
            map.moveActor(this, this.getBowserSpawnPoint());
        }
    }

}
