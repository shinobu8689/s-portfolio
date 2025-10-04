package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.player.Player;
import game.world.fountain.Fountain;

/**
 * for player to get water to the bottle when standing on fountain
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class RefillAction extends Action {

    /**
     * the fountain that player is getting the water
     */
    private Fountain fountain;

    /**
     * Constructor
     * @param fountain
     */
    public RefillAction(Fountain fountain){ this.fountain = fountain; }

    /**
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        Player player = ((Player) actor);
        player.getBottle().addWater(fountain.getWater());
        fountain.serveWater();
        return actor + " refills bottle from " + fountain.getClass().getSimpleName() + " " + fountain.displayServe();
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " refills " + fountain.getWater() + " " + fountain.displayServe();
    }
}
