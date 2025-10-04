package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.Utils;
import game.world.tree.Mature;
import game.world.tree.Sapling;
import game.world.tree.Sprout;
import game.world.Wall;
import edu.monash.fit2099.engine.positions.Ground;

/**
 * An action that attempts to jump the actor to a high ground location.
 *
 * @author Jasper Martin
 * @version 1.0
 */
public class JumpAction extends Action {
    // Target location
    private Location jumpToLocation;
    // Description of what happens to mario
    private String desc;
    // Direction of jump
    private String direction;

    /**
     * Constructor 
     * @param jumpToLocation target location
     * @param direction direction of jump
     */
    public JumpAction(Location jumpToLocation, String direction) {
        this.jumpToLocation = jumpToLocation;
        this.direction = direction;
    }
    /**
     * Allows actor to jump
     * @param actor actor jumping
     * @param map the game map
     * @return a description of what happened to the actor
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        // Gets the ground type that the actor is attemping to jump to
        Ground jumpToLocationType = jumpToLocation.getGround();
        // Calls the jump action with the percentage chance of success, as well as the fall damage
        // for failure
        if (jumpToLocationType instanceof Sprout) {
            Jump(actor, 90, 10, map, "Sprout");
        }
        else if (jumpToLocationType instanceof Sapling) {
            Jump(actor, 80, 20, map, "Sapling");
        }
        else if (jumpToLocationType instanceof Mature) {
            Jump(actor, 70, 30, map, "Mature");
        }
        else if (jumpToLocationType instanceof Wall) {
            Jump(actor, 80, 20, map, "Wall");
        }
        return this.desc;
    }

    /**
     * Returns a description of the movement for display in the menu
     * @param actor
     * @return A string e.g. "Player jumps West"
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + " jumps " + this.direction;
    }
    /**
     * Jumps the actor or applies fall damage
     * @param actor actor jumping
     * @param successRate percentage chance of success of jump
     * @param fallDamage damage taken by actor in case of failure
     * @param map gamemap
     * @param groundType string representation of type of ground actor is attempting to jump onto
     */

    private void Jump(Actor actor, int successRate, int fallDamage, GameMap map, String groundType) {
        // Checks if either the jump was a success or if the actor is TALL (100% success on jumps)
        // If so, moves the actor, and changes the description to the successful version
        if (Utils.randomChance(successRate) || actor.hasCapability(Status.TALL)) {
            map.moveActor(actor, this.jumpToLocation);
            this.desc = "Mario jumps up onto " + groundType;
        }
        // If the actor fails, then damages the actor, and changes the description to the 
        // failure description
        else {
            actor.hurt(fallDamage);
            this.desc = "Mario falls and takes " + fallDamage + " damage!";
        }
    }

    
}
