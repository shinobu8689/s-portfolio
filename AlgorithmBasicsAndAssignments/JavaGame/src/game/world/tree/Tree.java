package game.world.tree;

import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Resettable;
import game.Status;
import game.Utils;
import game.items.Coin;
import game.player.Player;
import edu.monash.fit2099.engine.actors.Actor;
import game.world.Dirt;
import game.world.JumpableGround;

/**
 * Abstract tree class from which types of trees are made.
 */
public abstract class Tree extends JumpableGround implements Resettable {

    protected Integer age;
    protected boolean dead = false;
    /**
     * Constructor.
     *
     */
    public Tree(Character symbol) {
        super(symbol);
        this.age = 0;
    }
    /**
     * if player is invincible they could destroy a wall and move to that location, $5 per tree
     * @param location The location of the Ground
     */
    public void tick(Location location){
        if (location.containsAnActor()){
            if (location.getActor() instanceof Player && location.getActor().hasCapability(Status.INVINCIBLE)){
                location.setGround(new Dirt());
                location.addItem(new Coin("Coin", '$', true, 5));
            }
        }
        killTree(location);
        super.tick(location);
    }
    /**
     * Kills tree (changes the ground back to dirt). Used for resetting the game and killing Mature trees
     * @param location location of tree
     */
    public void killTree(Location location) {
        if (this.dead) {
            location.setGround(new Dirt());
        }
    }

    public boolean blocksThrownObjects() {
        return true;
    }
    /**
     * Accessor of age 
     * @return age of tree
     */
    public Integer getAge() {
        return this.age;
    }


    @Override
    public void resetInstance(Actor actor, GameMap map) {
        if (Utils.randomChance(50)) {
            this.dead = true;
        }
    }

    @Override
    public void registerInstance() {
        Resettable.super.registerInstance();
    }
}
