package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.player.Player;

/**
 * Allows the player to quit the game
 *
 * @author Nethmini Botheju
 * @version 1.0
 */
public class QuitGameAction extends Action {
    /**
     * Perform the the action of quitting the game
     *
     * @param actor The actor performing the action.
     * @param map   The map the actor is on.
     * @return a description of what happened that can be displayed to the user.
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        if(actor instanceof Player) {

            map.removeActor(actor);
            return "Game has been quit!";
        }
        return null;
    }

    /**
     * Returns a descriptive string
     *
     * @param actor The actor performing the action.
     * @return the text we put on the menu
     */
    @Override
    public String menuDescription(Actor actor) {
        return "Quit Game";
    }
}
