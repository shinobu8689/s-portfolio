package game.behaviour;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Utils;
import game.actions.DrinkAction;
import game.world.fountain.Fountain;

import java.util.Random;

/**
 * figure can/should enemies drink water from the fountain
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class DrinkBehaviour extends Action implements Behaviour{

    /**
     * the fountain that enemy are drinking from
     */
    protected Fountain fountain;
    protected Integer drinkChance = 30;

    public DrinkBehaviour(Fountain fountain) {
        this.fountain = fountain;
    }

    @Override
    public String execute(Actor actor, GameMap map) {
        return menuDescription(actor);
    }

    @Override
    public String menuDescription(Actor actor) {
        return "Glub...Glub...";
    }

    @Override
    public Action getAction(Actor actor, GameMap map) {
        if (Utils.randomChance(drinkChance) && fountain != null && fountain.drinkable()) {
            return new DrinkAction(fountain);
        } else {
            return null;
        }
    }
}
