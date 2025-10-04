package game.enemies;


import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.ResetManager;
import game.Resettable;
import game.Status;
import game.behaviour.AggressiveBehaviour;
import game.behaviour.SuicideBehaviour;
import game.behaviour.WanderBehaviour;
/**
 * A little turtle guy.
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class Koopa extends Enemy {

    /**
     * Constructor.
     */
    public Koopa() {
        super("Koopa", 'k', 100);
        this.behaviours.put(10, new WanderBehaviour());
        this.behaviours.put(2, new AggressiveBehaviour());
        registerInstance();
    }

    @Override
    public char getDisplayChar(){
        return this.hasCapability(Status.DORMANT) ? 'D': super.getDisplayChar();
    }

    @Override
    protected IntrinsicWeapon getIntrinsicWeapon() {
        return new IntrinsicWeapon(30 + 15 * powerGauge, "punches");
    }


}
