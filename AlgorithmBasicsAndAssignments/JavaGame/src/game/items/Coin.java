package game.items;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Location;
import game.Resettable;
import game.Utils;
import game.player.Player;

/**
 * coin as currency
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class Coin extends BaseItem implements Resettable {

    private Integer value;
    private Boolean shouldDisappear = false;

    /**
     * Constructor.
     *
     * @param name the name of this Item
     * @param displayChar the character to use to represent this item if it is on the ground
     * @param portable true if and only if the Item can be picked up
     * @param value how much the coin is worth
     */
    public Coin(String name, char displayChar, boolean portable, Integer value){
        super(name, displayChar, portable);
        this.value = value;
        this.shouldDisappear = false;
        registerInstance();
    }

    /**
     * Constructor.
     * how much the coin is worth depends on the random value
     *
     * @param name the name of this Item
     * @param displayChar the character to use to represent this item if it is on the ground
     * @param portable true if and only if the Item can be picked up
     */
    public Coin(String name, char displayChar, boolean portable){
        super(name, displayChar, portable);
        this.value = Utils.randomIntCoin();
        registerInstance();
    }

    /**
     * Coin obj should not exist in player's inventory
     * in each turn, will add the value to player's wallet and remove the obj from player's inventory
     *
     * @param currentLocation The location of the actor carrying this Item.
     * @param actor The actor carrying this Item.
     */
    @Override
    public void tick(Location currentLocation, Actor actor) {
        ((Player) actor).pickUpCoins(value);
        actor.removeItemFromInventory(this);
    }

    /**
     * Inform an Item on the ground of the passage of time.
     * This method is called once per turn, if the item rests upon the ground.
     * @param currentLocation The location of the ground on which we lie.
     */
    public void tick(Location currentLocation) {
        if (shouldDisappear) {
            currentLocation.removeItem(this);
        }
        super.tick(currentLocation);
    }

    @Override
    public void resetInstance(Actor actor, GameMap map) {
        this.shouldDisappear = true;
    }

    @Override
    public void registerInstance() {
        Resettable.super.registerInstance();
    }
}
