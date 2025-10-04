package game.items;

import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.Location;
import edu.monash.fit2099.engine.weapons.WeaponItem;
import game.Maskable;

/**
 * new base for weapon that enable masking
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public abstract class BaseWeapon extends WeaponItem implements Maskable {
    /**
     * storing the default to show when unmasked
     */
    protected char defaultChar;

    public BaseWeapon(String name, char displayChar, int damage, String verb, int hitRate) {
        super(name, displayChar, damage, verb, hitRate);
        this.defaultChar = displayChar;
    }

    /**
     * Inform an Item on the ground of the passage of time.
     * This method is called once per turn, if the item rests upon the ground.
     * @param currentLocation The location of the ground on which we lie.
     */
    @Override
    public void tick(Location currentLocation) {
        Maskable.masking(currentLocation.map(), currentLocation,this);
    }

    public void setDefaultChar() {
        setDisplayChar(defaultChar);
    }

    public void setMaskedChar() { setDisplayChar(Maskable.fogChar); }
}
