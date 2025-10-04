package game.npc;

import edu.monash.fit2099.engine.actions.DoNothingAction;
import game.Status;
import game.actions.FreePeachAction;
import game.items.PeachKey;
import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.GameMap;

public class PrincessPeach extends Actor {
/**
 * The princess that mario always seems to want to be with
 */
   public PrincessPeach() {
       super("Princess Peach", 'P', 1000000); // Peach shouldn't be able to die
       this.addCapability(Status.INVINCIBLE); // This also helps not dying

   }
/**
 * Checks if the player has the key to Peach's handcuffs in their inventory
 * If so, then they can free the princess
 * @param player The player
 * @param direction The direction (redundant)
 * @param map the game map
 */
    public ActionList allowableActions(Actor player, String direction, GameMap map) {
        ActionList actions = new ActionList();
        for (Item item : player.getInventory()) {
            if (item instanceof PeachKey) {
                actions.add(new FreePeachAction());
            }
        }
        return actions;
    }


    @Override
    /**
     * Forces the princess to do nothing every turn, as she is trapped and cannot move
     * 
     */
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {
        return new DoNothingAction();
    }
}
