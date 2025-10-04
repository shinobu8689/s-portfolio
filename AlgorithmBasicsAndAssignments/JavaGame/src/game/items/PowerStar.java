package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.actions.ConsumeItemAction;
import game.player.Player;

/**
 * let player be invincible
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class PowerStar extends BaseItem implements Consumable, Tradeable{
    private int price = 600;
    /**
     * the remaining turn that until fade out
     */
    private Integer remainingTurn;

    /**
     * how long will the Status.INVINCIBLE last
     */
    private Integer effectDuration;

    /***
     * Constructor.
     *
     *  @param name the name of this Item
     * @param displayChar the character to use to represent this item if it is on the ground
     * @param portable true if and only if the Item can be picked up
     */
    public PowerStar(String name, char displayChar, boolean portable, Integer remainingTurn, Integer effectDuration) {
        super(name, displayChar, portable);
        this.remainingTurn = remainingTurn + 1; // these are given with an extra turn because the games count the turn you buy or consume it as one turn as well
        this.effectDuration = effectDuration + 1;
        this.addAction(new ConsumeItemAction(this));
    }

    /**
     * decrease 1 turn since PowerStar is created on the ground
     * remove itself after 10 turns, leaving a coin behind
     * @param currentLocation The location of the ground on which we lie.
     */
    @Override
    public void tick(Location currentLocation) {
        remainingTurn -= 1;
        if (remainingTurn == 0) {
            currentLocation.removeItem(this);
        }
        super.tick(currentLocation);
    }

    /**
     * decrease 1 turn since PowerStar is created on the ground
     * remove itself after 10 turns, leaving $5 to the player
     * @param currentLocation The location of the ground on which we lie.
    */
    @Override
    public void tick(Location currentLocation, Actor actor) {
        remainingTurn -= 1;
        if (remainingTurn == 0) {
            actor.removeItemFromInventory(this);
        }
    }

    public String toStringWithTurn(){
        return this + " - " + getRemainingTurn() + " turns remaining";
    }

    public Integer getRemainingTurn() {
        return remainingTurn;
    }
    public Integer getEffectDuration() { return effectDuration; }

    public void consumeBy(Player player){
        player.addCapability(Status.INVINCIBLE);
        player.heal(200);
        player.setInvincibleCounter(getEffectDuration());
    }

    public boolean calculateTrade(Player actor){
        int amount;
        amount = actor.getWallet();
        if (amount - this.price >= 0) {
            actor.subTradeWallet(price);
            actor.addItemToInventory(this);
            return true;
        } else {
            return false;
        }
    }

    public int getPrice() {
        return this.price;
    }
}
