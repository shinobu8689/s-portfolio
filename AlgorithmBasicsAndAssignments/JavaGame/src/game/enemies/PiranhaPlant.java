package game.enemies;

import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.weapons.IntrinsicWeapon;
import game.Resettable;
import game.actions.AggressiveAction;
import game.behaviour.AggressiveBehaviour;
import game.behaviour.AttackBehaviour;
import game.player.Player;
import edu.monash.fit2099.engine.actors.Actor;

public class PiranhaPlant extends Enemy {
    /**
     * A nasty sub-species of the venus flytrap that is rather larger.
     */
    public PiranhaPlant() {
        super("Piranha Plant", 'Y', 150);
        this.behaviours.put(2, new AggressiveBehaviour());
        registerInstance();       
    }

    @Override
    protected IntrinsicWeapon getIntrinsicWeapon() {
        return new IntrinsicWeapon(90 + 15 * powerGauge, "chomps");
    }

    @Override
    public void resetInstance(Actor actor, GameMap map) {
        this.behaviours.clear();
        this.increaseMaxHp(50);
    }

    @Override
    /**
     * Changes the aggression logic so that the plant can become agressive and attack
     * the player, but it cannot chase them, as it is stuck in a pot. 
     * @param target the target of aggressions (the player)
     */
    public void toAggressive(Actor target) {
        this.behaviours.put(4, new AttackBehaviour(target));
        this.behaviours.remove(2);
    }
}
