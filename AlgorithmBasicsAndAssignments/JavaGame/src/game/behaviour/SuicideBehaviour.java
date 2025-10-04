package game.behaviour;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Utils;
import game.actions.SuicideAction;

import java.util.Random;

/**
 * decide should goomba kill himself
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class SuicideBehaviour extends Action implements Behaviour {

    protected Integer rateToBeKilled;

    public SuicideBehaviour() { this.rateToBeKilled = 10; }

    /**
     * Returns a SuicideAction if in 10%, or force suicide when resetting.
     * If no movement is possible, returns null.
     *
     * @param actor the Actor enacting the behaviour
     * @param map the map that actor is currently on
     * @return an Action, or null if no MoveAction is possible
     */
    @Override
    public Action getAction(Actor actor, GameMap map) {
        if (Utils.randomChance(rateToBeKilled)){
            return new SuicideAction();
        } else {
            return null;
        }
    }

    @Override
    public String execute(Actor actor, GameMap map) { return menuDescription(actor); }

    @Override
    public String menuDescription(Actor actor) { return "Raagrh..."; }
}
