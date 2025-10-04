package game.behaviour;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Utils;
import game.actions.AttackAction;

public class AttackBehaviour extends Action implements Behaviour {

    /**
     * the actor who will get attacked
     */
    private final Actor target;

    private double range = 1.5; //~sqrt(2)

    public AttackBehaviour(Actor subject) { this.target = subject; }

    /**
     * Returns a AttackAction if player is in reach of enemies
     * If no movement is possible, returns null.
     *
     * @param actor the Actor enacting the behaviour
     * @param map the map that actor is currently on
     * @return an Action, or null if no MoveAction is possible
     */
    @Override
    public Action getAction(Actor actor, GameMap map) {
        Location here = map.locationOf(actor);
        Location there = map.locationOf(target);

        if(Utils.distance(here,there) > range){
            return null;
        } else {
            return new AttackAction(target);
        }
    }

    @Override
    public String execute(Actor actor, GameMap map) { return null; }

    @Override
    public String menuDescription(Actor actor) { return "Raagrh!"; }

}
