package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.ResetManager;
import game.Status;
import game.WarpMapManager;
import game.enemies.Bowser;
import game.player.Player;
import game.world.LavaMap;

/**
 * Allows the player to replay the game if unconscious
 *
 * @author Nethmini Botheju
 * @version 1.0
 */
public class ReplayAction extends Action {


    /**
     * Perform the action of allowing the player to replay the game
     *
     * @param actor The actor performing the action.
     * @param map   The map the actor is on.
     * @return a description of what happened that can be displayed to the user.
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        if(actor.hasCapability(Status.PLAYABLE)) {
            Player player = (Player) actor;
            player.getLives().loseLife();
            ResetManager.getInstance().run(player, map);

            if (map instanceof LavaMap) {
                Location pipeLocation = WarpMapManager.newWarpLocation;
                map.moveActor(player, pipeLocation);
            } else {
                map.moveActor(player, player.getSpawnPoint());
                }

            return player + " replays the game!";
        }else if(actor.hasCapability(Status.FINAL_BOSS)){
            Bowser bowser = (Bowser) actor;
            ResetManager.getInstance().run(bowser, map);
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
        return "Play again";
    }
}
