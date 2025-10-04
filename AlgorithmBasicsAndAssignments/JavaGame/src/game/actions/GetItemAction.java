package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.ResetManager;
import game.Status;


/**
 * Class for player get free items from Toad
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class GetItemAction extends Action {

    /**
     * the item that player will get
     */
    protected Item item;

    /**
     * Constructor
     * @param item
     */
    public GetItemAction(Item item){
        this.item = item;
    }

    /**
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a suitable description to display in the UI
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        if (actor.hasCapability(Status.CAN_TRADE)) {
            actor.addItemToInventory(item);
            return actor + " gets " + item + "!";
        }
        return actor + "gets nothing!";
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " gets " + item;
    }

}
