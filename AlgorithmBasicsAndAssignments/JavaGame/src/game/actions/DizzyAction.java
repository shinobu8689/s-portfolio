package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;
import game.Utils;
import game.behaviour.WanderBehaviour;

/**
 * the only action that player can do when dizzy or not conscious
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class DizzyAction extends Action {

    /**
     *  the chance that player could wake up
     */
    private final Integer wakeUpChance = 40;

    /**
     * get random direction from WanderBehaviour
     */
    private WanderBehaviour wanderBehaviour = new WanderBehaviour();

    /**
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        String result = null;

        if (Utils.randomChance(wakeUpChance)) {
            result = actor + " wakes up";
            actor.removeCapability(Status.DIZZY);
        } else {
            result = wanderBehaviour.getAction(actor, map).execute(actor, map);
            // game over if player is not conscious and no luck at the last chance to be awake
            if (!actor.isConscious()){ map.removeActor(actor); }
        }
        return result;
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " tries to wake up";
    }
}
