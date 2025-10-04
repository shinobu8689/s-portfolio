package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;
import game.items.Tradeable;
import game.player.Player;

/**
 * Class for player to trade magical items and weapons with Toad
 *
 * @author Nethmini Botheju
 * @version 2.0
 * @see edu.monash.fit2099.engine.actions.Action
 */
public class TradeAction extends Action {
    Tradeable item;

    /**
     * Constructor
     */
    public TradeAction(Item item) {
        this.item = (Tradeable) item;
    }

    /**
     * Constructor method for the TradeAction class
     *
     */

    /**
     * Perform the action of trading with toad for the item requested by the player
     *
     * @see Action#execute(Actor, GameMap)
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a string depending on if the trade was successful or not
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        if (actor.hasCapability(Status.CAN_TRADE)){
            if (item.calculateTrade((Player)actor)) {
                return actor + " has bought " + item.toString() + "!";
            } else {
                return "You don't have enough coins!";
            }
        }
        return actor + " cannot Trade!";
    }

    /**
     * Describe the action for player to input to buy certain items
     *
     * @param actor The actor performing the action.
     * @return a string of the item bought by the actor
     */
    @Override
    public String menuDescription(Actor actor){
        return  actor + " buys " + item.toString() + " ($"+ item.getPrice()+")";
    }

    /**
     * Calculates the change when the trade is done with the wallet amount and item cost
     *
     * @param actor the actor that is doing the trade
     * @return boolean true or false depending on if the trade was successful or not
     */
}

