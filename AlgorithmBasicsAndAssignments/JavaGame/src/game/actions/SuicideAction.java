package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.enemies.Enemy;
import game.enemies.Koopa;

/**
 * Special Action for Actors(Goomba) to despawn(suicide).
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class SuicideAction extends Action {

    /**
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        ((Enemy) actor).instantKill();

        if (!actor.isConscious()) {
            ActionList dropActions = new ActionList();
            // drop all items
            for (Item item : actor.getInventory())
                dropActions.add(item.getDropAction(actor));
            for (Action drop : dropActions)
                drop.execute(actor, map);
            // remove actor
            map.removeActor(actor);
        }

        return menuDescription(actor);
    }

    /**
     * Describe the action in a format suitable for displaying in the menu.
     * @param actor The actor performing the action.
     * @return a string, e.g. "Player picks up the rock"
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + " is killed";
    }
}
