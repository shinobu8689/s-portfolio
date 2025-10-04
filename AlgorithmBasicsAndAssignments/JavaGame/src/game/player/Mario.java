package game.player;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;

public class Mario extends Player {
    /**
     * Constructor to create mario
     */
    public Mario() {
        super("Mario", 'm', 100, 3);
    }

    /**
     * Mario's unique trait is more damage than Luigi
     * @return attack damage string
     */
    @Override
    protected IntrinsicWeapon getIntrinsicWeapon() {
        return new IntrinsicWeapon(10 + 15 * powerGauge, "punches");
    }

}
