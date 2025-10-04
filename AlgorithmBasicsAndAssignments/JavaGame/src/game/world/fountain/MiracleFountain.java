package game.world.fountain;

import edu.monash.fit2099.engine.positions.Location;
import game.Utils;
import game.water.BlessedWater;
import game.water.ShieldWater;

import java.util.Random;
/**
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class MiracleFountain extends Fountain {

    private Integer switchWaterChance = 50;

    // 50% to switch to another type if water
    public MiracleFountain() {
        super('V');
        if (Utils.randomChance(switchWaterChance)) {
            setWater(new BlessedWater());
        } else {
            setWater(new ShieldWater());
        }
    }

    /**
     * Ground can also experience the joy of time.
     * @param location The location of the Ground
     */
    @Override
    public void tick(Location location) {
        super.tick(location);
        // 50% to switch to another type if water
        if (Utils.randomChance(switchWaterChance)) {
            if (this.getWater() instanceof BlessedWater){
                setWater(new ShieldWater());
            } else {
                setWater(new BlessedWater());
            }
        }
    }
}
