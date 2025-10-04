package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.items.Bottle;
import game.items.Consumable;
import game.player.Player;
import game.items.PowerStar;

/**
 * Special Action for consuming item for Player's only.
 *
 * @author Yin Lam Lo
 * @version 2.0
 */
public class ConsumeItemAction extends Action {

    /**
     *  the item that actor consume
     */
    private final Consumable item;

    private String verb = " consume ";

    /**
     * Constructor.
     *
     * @param item the item to consume by Player
     */
    public ConsumeItemAction(Consumable item) { this.item = item; }

    /**
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {

        if (item instanceof Consumable && actor instanceof Player) {
            item.consumeBy(((Player) actor));
        }

        // consume the item from inventory first, then the one on the ground
        if (!(item instanceof Bottle)) {
            if (actor.getInventory().contains(item)) {
                actor.removeItemFromInventory((Item)item);
            } else {
                map.locationOf(actor).removeItem((Item)item);
            }
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
        if (item instanceof PowerStar){
            return actor + verb + ((PowerStar) item).toStringWithTurn();
        } else if (item instanceof Bottle){
            return actor + verb + "Water";
        } else {
            return actor + verb + item;
        }
    }

}
