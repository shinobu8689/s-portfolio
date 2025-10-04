package game.world;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.Resettable;
import game.Status;
import game.actions.WarpAction;
import game.enemies.PiranhaPlant;
import game.player.Player;

/**
 * Class that creates the WarpPipe from the ground
 *
 * @author Nethmini Botheju
 * @version 1.0
 * @see edu.monash.fit2099.engine.positions.Ground
 */
public class WarpPipe extends BaseGround implements Resettable {

    private int age;
    /**
     * Constructor for creating the WarpPipe object
     */
    public WarpPipe() {
        super('C');
        this.addCapability(Status.WARPABLE);
        this.age = 1;
        registerInstance();
    }

    /**
     * checks if the actor is a player to enter
     *
     * @param actor the Actor to check
     * @return boolean true or false
     */
    public boolean canActorEnter(Actor actor) {
        if (actor instanceof Player){
            return true;
        } else {
            return false;
        }
    }

    @Override
    /**
     * Allows the pipe to feel the flow of time, and so spawn a piranha plant every time it turns 2.
     * This happens at the start of the game, as well as whenever the game gets reset. 
     * @param location the location of the warp pipe
     */
    public void tick(Location location) {
        super.tick(location);
        age++;
        if (age == 2 && !location.containsAnActor()) {
            location.addActor(new PiranhaPlant());
        }
    }
    /**
     * adds the warp action to its actions list
     *
     * @param actor the Actor acting
     * @param location the current Location
     * @param direction the direction of the Ground from the Actor
     * @return actions list
     */
    public ActionList allowableActions(Actor actor, Location location, String direction){
        ActionList actions = new ActionList();
        if(location.containsAnActor()) {
            actions.add(new WarpAction());
        }
        return actions;

    }

    @Override
    public void resetInstance(Actor actor, GameMap map) {
        this.age = 1; // Set age back to 1 so that piranha plants will respawn when the game is reset
    }


}
