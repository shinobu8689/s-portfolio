package game.enemies;


import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.Resettable;
import game.behaviour.*;


/**
 * A little fungus guy.
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public class Goomba extends Enemy {

	/**
	 * Constructor.
	 */
	public Goomba() {
		super("Goomba", 'g', 20);
		this.behaviours.put(10, new WanderBehaviour());
		this.behaviours.put(2, new AggressiveBehaviour());
		this.behaviours.put(1,new SuicideBehaviour());
		registerInstance();
	}

	@Override
	protected IntrinsicWeapon getIntrinsicWeapon() {
		return new IntrinsicWeapon(10 + 15 * powerGauge, "kicks");
	}

}
