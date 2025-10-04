package game.world;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.actors.Actor;
import game.Status;
import game.actions.JumpAction;

/**
 * Intermediary class between ground and any types of ground that need to be jumped to.
 * Implements some methods that are universal to these types of ground.
 */
public abstract class JumpableGround extends BaseGround {
    /**
     * Constructor.
     * @param symbol symbol of ground passed to parent
     */
    public JumpableGround(Character symbol) {
        super(symbol);
    }



    @Override
    public boolean canActorEnter(Actor actor) {
        // actors can enter if in god-mod (invincible) or if they can fly
        if (actor.hasCapability(Status.INVINCIBLE) || actor.hasCapability(Status.FLYING)) {
            return true;
        } else {
            return false;
        }
        }
    
    /**
     * Method to add the JumpAction to the location if it should be there
     * @param actor the player
     * @param location the location of the ground being jumped to
     * @param direction the direction of the location from the players current location
     * @return an actionlist that has the appropriate action in it to add to the player's possible actions
     */
    @Override
    public ActionList allowableActions(Actor actor, Location location, String direction) {
        // If the location is not the one that the actor is currently standing on, and the player is
        // not invulnerable, adds a JumpAction to the location
        // If player is invulnerable, they will simply be able to walk onto the location, instead of having to jump
        if (direction.length() > 0 && !actor.hasCapability(Status.INVINCIBLE)) {
            return new ActionList(new JumpAction(location, direction));
        }
        else {
            return new ActionList();
        }
    }
}
