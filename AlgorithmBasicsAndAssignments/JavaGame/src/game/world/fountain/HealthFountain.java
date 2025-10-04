package game.world.fountain;

import game.water.HealthWater;

/**
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class HealthFountain extends Fountain {

    public HealthFountain() {
        super('H');
        setWater(new HealthWater());
    }
}
