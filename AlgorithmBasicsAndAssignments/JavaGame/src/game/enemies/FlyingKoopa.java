package game.enemies;

import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.Resettable;
import game.Status;
import game.behaviour.AggressiveBehaviour;
import game.behaviour.WanderBehaviour;

public class FlyingKoopa extends Enemy {
    /**
     * A class representing a flying version of the Koopa
     */
    public FlyingKoopa() {
        super("Flying Koopa", 'F', 150);
        this.behaviours.put(10, new WanderBehaviour());
        this.behaviours.put(2, new AggressiveBehaviour());
        this.addCapability(Status.FLYING); // Look ma!
        registerInstance();
    }

    @Override
    public char getDisplayChar() {
        return this.hasCapability(Status.DORMANT) ? 'D': super.getDisplayChar();
    }

    @Override
    protected IntrinsicWeapon getIntrinsicWeapon() {
        return new IntrinsicWeapon(30 + 15 * powerGauge, "swoops");
    }
}
