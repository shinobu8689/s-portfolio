package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.ResetManager;

/**
 * Special Action for player to reset the world.
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class ResetAction extends Action {

    protected String hotKey;

    public ResetAction() {
        this.hotKey = "r";
    }

    /**
     *
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        ResetManager.getInstance().run(actor, map);
        return actor + " has reset the map!";
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " resets game";
    }

    @Override
    public String hotkey() {
        return hotKey;
    }

}
