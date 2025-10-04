package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.enemies.Enemy;
import game.water.HealthWater;
import game.water.PowerWater;
import game.world.fountain.Fountain;
import game.world.fountain.HealthFountain;
import game.world.fountain.PowerFountain;


/**
 * for enemies to drink water near the fountain
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class DrinkAction extends Action {

    /**
     * the fountain that the enemy are drinking from
     */
    private Fountain fountain;

    /**
     * Constructor
     * @param fountain to see which fountain it drinks from
     */
    public DrinkAction(Fountain fountain){
        this.fountain = fountain;
    }

    /**
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        Enemy enemy = ((Enemy) actor);
        if (fountain.getWater() instanceof HealthWater) {
            enemy.drinkHealthWater();
        } else if (fountain.getWater() instanceof PowerWater) {
            enemy.drinkPowerWater();
        }
        fountain.serveWater();

        return menuDescription(actor);
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " drinks "+ fountain.getWater();
    }
}
