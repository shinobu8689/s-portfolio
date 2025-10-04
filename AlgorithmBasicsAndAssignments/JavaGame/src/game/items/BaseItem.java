package game.items;

import edu.monash.fit2099.engine.items.Item;
import edu.monash.fit2099.engine.positions.Location;
import game.Maskable;

/**
 * new base for item that enable masking
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public abstract class BaseItem extends Item implements Maskable {
    /**
     * storing the default to show when unmasked
     */
    private char defaultChar;

    /***
     * Constructor.
     *  @param name the name of this Item
     * @param displayChar the character to use to represent this item if it is on the ground
     * @param portable true if and only if the Item can be picked up
     */
    public BaseItem(String name, char displayChar, boolean portable) {
        super(name, displayChar, portable);
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

    public void setMaskedChar() {
        setDisplayChar(Maskable.fogChar);
    }


}
