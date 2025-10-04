package game;

import edu.monash.fit2099.engine.actors.Actor;

/**
 * Refactored that shared attribute and method for functions
 *
 * @author Yin Lam Lo
 * @version 1.0
 */

public abstract class BaseActor extends Actor {

    //for how many PowerWater drunk
    protected Integer powerGauge;


    /**
     * Constructor.
     *
     * @param name        the name of the Actor
     * @param displayChar the character that will represent the Actor in the display
     * @param hitPoints   the Actor's starting hit points
     */
    public BaseActor(String name, char displayChar, int hitPoints) {
        super(name, displayChar, hitPoints);
        this.powerGauge = 0;
    }

    /**
     * Heal actor to full
     * @return how much Health it will heal to
     */
    public Integer healMaximum(){
        heal(getMaxHp());
        return getMaxHp();
    }

    /**
     * instant Kill enemies
     * @return how much damage it deal
     */
    public Integer instantKill(){
        this.hurt(getMaxHp());
        return getMaxHp();
    }

    public void drinkHealthWater(){ this.heal(50); }

    public void drinkPowerWater(){
        this.powerGauge += 1;
    }

}
