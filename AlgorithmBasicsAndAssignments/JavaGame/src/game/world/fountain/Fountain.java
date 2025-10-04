package game.world.fountain;

import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Location;
import game.actions.RefillAction;
import game.player.Player;
import game.water.StandardWater;
import game.world.BaseGround;

/**
 * fountain base for different types of fountain
 *
 * @author Yin Lam Lo
 * @version 1.0
 */
public abstract class Fountain extends BaseGround {

    /**
     * the max amount of servings
     */
    private final Integer defaultRemainingServe = 10;

    /**
     * the type of water it serves
     */
    private StandardWater water;

    /**
     * the serve remaining inside the fountain
     */
    private Integer remainingServe;

    /**
     * the remaining turn to replenish
     */
    private Integer refillTimer;

    /**
     * is it replenishing
     */
    private Boolean replenish;

    /**
     * Constructor.
     *
     * @param displayChar character to display for this type of terrain
     */
    public Fountain(char displayChar) {
        super(displayChar);
        remainingServe = defaultRemainingServe;
        refillTimer = 0;
    }

    protected void setWater(StandardWater water){
        this.water = water;
    }

    public StandardWater getWater(){
        return this.water;
    }

    public void serveWater(){
        this.remainingServe -= 1;
    }

    /**
     * Ground can also experience the joy of time.
     * @param location The location of the Ground
     */
    public void tick(Location location) {
        super.tick(location);
        if (this.refillTimer > 0) { this.refillTimer -= 1; }
        if (this.remainingServe == 0) { this.refillTimer = 5; }
        if (this.refillTimer == 0) { replenish = true; }
        if (replenish && remainingServe == 0) {
            remainingServe = defaultRemainingServe;
            replenish = false;
        }
    }

    /**
     * let the enemies know can they drink from this fountain
     * @return is it drinkable
     */
    public Boolean drinkable(){ return this.remainingServe > 0 && this.refillTimer == 0; }

    /**
     * Returns an empty Action list.
     *
     * @param actor the Actor acting
     * @param location the current Location
     * @param direction the direction of the Ground from the Actor
     * @return a new, empty collection of Actions
     */
    public ActionList allowableActions(Actor actor, Location location, String direction) {
        if (location.getActor() instanceof Player && ((Player) actor).hasBottle() && this.drinkable() && location.containsAnActor()) {
            return new ActionList(new RefillAction(this));
        } else {
            return new ActionList();
        }
    }

    public String displayServe(){
        return "(" + remainingServe + "/" + defaultRemainingServe + ")";
    }
}
