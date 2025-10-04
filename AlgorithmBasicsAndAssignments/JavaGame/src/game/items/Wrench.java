package game.items;

import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.weapons.Weapon;
import edu.monash.fit2099.engine.weapons.WeaponItem;
import game.Maskable;
import game.player.Player;

/**
 * wrench weapon that could destroy koopa shell
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class Wrench extends BaseWeapon implements Weapon, Maskable, Tradeable {
    private int price = 200;
    /**
     * Constructor.
     *
     * @param name        name of the item
     * @param displayChar character to use for display when item is on the ground
     * @param damage      amount of damage this weapon does
     * @param verb        verb to use for this weapon, e.g. "hits", "zaps"
     * @param hitRate     the probability/chance to hit the target.
     */
    public Wrench(String name, char displayChar, int damage, String verb, int hitRate) {
        super(name, displayChar, damage, verb, hitRate);
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
        return price;
    }
}
