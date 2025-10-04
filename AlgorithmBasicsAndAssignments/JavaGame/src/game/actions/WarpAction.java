package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.WarpMapManager;
import game.player.Player;

import static game.WarpMapManager.getWarpableMap;

/**
 * Class that creates the Warp Pipe to move from map to map
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class WarpAction extends Action {
    WarpMapManager warpMapManager = WarpMapManager.getInstance();
    /**
     * Perform the Action.
     *
     * @param actor The actor performing the action.
     * @param map   The map the actor is on.
     * @return a description of what happened that can be displayed to the user.
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        Player player = (Player) actor;
        GameMap lavaMap = getWarpableMap("LavaMap");
        return warpMapManager.newWarpLocation(map, lavaMap, player);
    }

    /**
     * Returns a descriptive string
     *
     * @param actor The actor performing the action.
     * @return the text we put on the menu
     */
    @Override
    public String menuDescription(Actor actor) {
        return  actor + " uses Warp Pipe";
    }
}
