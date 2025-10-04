package game.items;

import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.actions.ConsumeItemAction;
import game.player.Player;

/**
 * eat super mushroom to have buffs to the player
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class SuperMushroom extends BaseItem implements Consumable, Tradeable{
    private int price = 400;
    /***
     * Constructor.
     *  @param name the name of this Item
     * @param displayChar the character to use to represent this item if it is on the ground
     * @param portable true if and only if the Item can be picked up
     */
    public SuperMushroom(String name, char displayChar, boolean portable) {
        super(name, displayChar, portable);
        this.addAction(new ConsumeItemAction(this));
    }

    /**
     * Inform an Item on the ground of the passage of time.
     * This method is called once per turn, if the item rests upon the ground.
     * @param currentLocation The location of the ground on which we lie.
     */
    @Override
    public void tick(Location currentLocation) {
        super.tick(currentLocation);
    }

    public void consumeBy(Player player){
        player.addCapability(Status.TALL);
        player.increaseMaxHp(50);
        player.healMaximum();
    }

    public boolean calculateTrade(Player actor){
        int amount;
        amount = actor.getWallet();
        if (amount - this.price >= 0) {
            actor.subTradeWallet(price);
            actor.addItemToInventory(this);
            return true;
        }
        return false;
    }


    public int getPrice() {
        return this.price;
    }
}