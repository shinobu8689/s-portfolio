package game.behaviour;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.ResetManager;
import game.Status;
import game.actions.AggressiveAction;
/**
 * decide should enemies become aggressive
 *
 * @author Yin Lam Lo
 * @version 2.0
 */
public class AggressiveBehaviour extends Action implements Behaviour {

    private Actor target;

    public AggressiveBehaviour() {}

    /**
     * Returns a AggressiveAction to make enemy trying to follow and attack player, if possible.
     * If no movement is possible, returns null.
     *
     * @param actor the Actor enacting the behaviour
     * @param map the map that actor is currently on
     * @return an Action, or null if no MoveAction is possible
     */
    @Override
    public Action getAction(Actor actor, GameMap map) {
        // find the player nearby, if there is a player start follow and attack him
        for (Exit exit : map.locationOf(actor).getExits()) {
            Location destination = exit.getDestination();
            if (destination.containsAnActor() && destination.getActor().hasCapability(Status.HOSTILE_TO_ENEMY)) {
                this.target = destination.getActor();
                return new AggressiveAction(target);
            }
        }
        return null;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        return menuDescription(actor);
    }

    @Override
    public String menuDescription(Actor actor) { return "Raagrh!"; }

}
