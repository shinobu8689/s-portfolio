package game.npc;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.GameMap;
import game.actions.GetItemAction;
import game.actions.SpeakAction;
import game.actions.TradeAction;
import game.items.*;
import game.player.Player;

/**
 * Class for player to trade magical items and weapons with Toad
 *
 * @author Nethmini Botheju
 * @version 2.0
 * @see SpeakAction
 * @see game.actions.TradeAction
 */
public class Toad extends Actor {
    /**
     * Constructor for Toad using Actor as superclass
     *
     */
    public Toad() {
        super("Toad", 'O', 1000);
    }

    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {
        ActionList actions = new ActionList();
        actions.add(new SpeakAction());
        actions.add(new TradeAction(new PowerStar("Power Star",'*',false,10, 10)));
        actions.add(new TradeAction(new SuperMushroom("Super Mushroom",'^',false)));
        actions.add(new TradeAction(new Wrench("Wrench", 'w', 50, "wreck", 80)));
        if (!((Player) otherActor).hasBottle()) {
            actions.add(new GetItemAction(new Bottle("Bottle",'b',false)));
        }
        return actions;
    }

    @Override
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
        return new DoNothingAction();
    }
}
