package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.weapons.Weapon;
import game.ResetManager;
import game.Status;
import game.Utils;
import game.enemies.FlyingKoopa;
import game.enemies.Koopa;
import game.items.SuperMushroom;

import java.util.Random;

/**
 * Special Action for removing actor that has dormant capability.
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class BreakShellAction extends Action {

    /**
     * The Actor(Koopa)'s shell that is to be destroyed
     */
    protected Actor target;

    /**
     * The direction of incoming attack.
     */
    protected String direction;

    /**
     * Constructor.
     *
     * @param target the Actor to destroy the shell
     */
    public BreakShellAction(Actor target, String direction) {
        this.target = target;
        this.direction = direction;
    }

    /**
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {

        Weapon weapon = actor.getWeapon();

        if (Utils.randomChance(100 - weapon.chanceToHit())) {
            return actor + " misses " + target + ".";
        }

        // destroy shell and leave a mushroom if the target is a dormant koopa
        if ((target instanceof Koopa || target instanceof FlyingKoopa) && target.hasCapability(Status.DORMANT)){
            map.locationOf(target).addItem(new SuperMushroom("Super Mushroom", '^',true));
            map.removeActor(target);
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
        return actor + " breaks " + target + "'s shell at " + direction;
    }
}
