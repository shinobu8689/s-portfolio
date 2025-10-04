package game.world.fountain;

import game.water.PowerWater;

/**
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class PowerFountain extends Fountain {
    public PowerFountain() {
        super('A');
        setWater(new PowerWater());
    }
}
