package game.world;

import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.Maskable;

/**
 * the base of the ground that enable to mask
 * @author Yin Lam Lo
 * @version 1.0
 */
public abstract class BaseGround extends Ground implements Maskable {

    private char defaultChar;

    /**
     * Constructor.
     *
     * @param displayChar character to display for this type of terrain
     */
    public BaseGround(char displayChar) {
        super(displayChar);
        this.defaultChar = displayChar;
    }

    /**
     * Ground can also experience the joy of time.
     * @param location The location of the Ground
     */
    public void tick(Location location) {
        GameMap map = location.map();
        Maskable.masking(map, location, this);
    }

    public void setDefaultChar() {
        setDisplayChar(defaultChar);
    }

    public void setMaskedChar() {
        setDisplayChar(Maskable.fogChar);
    }
}
