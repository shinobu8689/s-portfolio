package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.enemies.Enemy;

/**
 * Action to let enemies be aggressive to player.
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class AggressiveAction extends Action {

    protected Actor target;

    /**
     * Constructor.
     *
     * @param target the Actor that NPC noticed
     */
    public AggressiveAction(Actor target) {	this.target = target; }

    /**
     *
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        ((Enemy) actor).toAggressive(this.target);
        return menuDescription(actor);
    }

    /**
     * Describe the action in a format suitable for displaying in the menu.
     *
     * @see Action#menuDescription(Actor)
     * @param actor The actor performing the action.
     * @return a string, e.g. "Player picks up the rock"
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + " notices " + target;
    }
}
