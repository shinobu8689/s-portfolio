package game.enemies;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actions.ActionList;
import edu.monash.fit2099.engine.actions.DoNothingAction;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.displays.Display;
import edu.monash.fit2099.engine.positions.Exit;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.positions.Ground;
import game.*;
import game.actions.AttackAction;
import game.actions.BreakShellAction;
import game.actions.SuicideAction;
import game.behaviour.*;
import game.items.Wrench;
import game.world.fountain.Fountain;

import java.util.HashMap;
import java.util.Map;

/**
 * The base class for any enemies
 *
 * @author Yin Lam Lo
 * @version 2.0
 */
public abstract class Enemy extends BaseActor implements Resettable, Maskable {

    /**
     *  1) SuicideBehaviour
     *  2) AggressiveBehaviour
     *  3) DrinkWaterBehaviour
     *  4) AttackBehaviour
     *  5) FollowBehaviour
     */
    protected final Map<Integer, Behaviour> behaviours = new HashMap<>(); // priority, behaviour

    /**
     * storing the default to show when unmasked
     */
    private char defaultChar;

    /**
     * Constructor.
     *
     * @param name        the name of the Enemy
     * @param displayChar the character that will represent the Actor in the display
     * @param hitPoints   the Actor's starting hit points
     */
    public Enemy(String name, char displayChar, int hitPoints) {
        super(name, displayChar, hitPoints);
        this.defaultChar = displayChar;
    }

    /**
     * @param otherActor the Actor that might perform an action.
     * @param direction  String representing the direction of the other Actor
     * @param map        current GameMap
     * @return list of actions
     * @see Status#HOSTILE_TO_ENEMY
     */
    @Override
    public ActionList allowableActions(Actor otherActor, String direction, GameMap map) {
        ActionList actions = new ActionList();
        // it can be attacked only by the HOSTILE opponent, and this action will not attack the HOSTILE enemy back.
        if(otherActor.hasCapability(Status.HOSTILE_TO_ENEMY) && !this.hasCapability(Status.DORMANT)) {
            actions.add(new AttackAction(this, direction));
        }

        if (this.hasCapability(Status.DORMANT) && otherActor.getWeapon() instanceof Wrench){
            actions.add(new BreakShellAction(this,direction));
        }

        return actions;
    }

    /**
     * Figure out what to do next.
     * @see Actor#playTurn(ActionList, Action, GameMap, Display)
     */
    @Override
    public Action playTurn(ActionList actions, Action lastAction, GameMap map, Display display) {

        Maskable.masking(map, map.locationOf(this), this);

        // can drink water when near fountain
        for (Exit exit : map.locationOf(this).getExits()) {
            Ground ground = exit.getDestination().getGround();
            if (ground instanceof Fountain) {
                this.behaviours.put(3, new DrinkBehaviour((Fountain) ground));
            } else {
                this.behaviours.remove(3);
            }
        }

        for(Behaviour behaviour : behaviours.values()) {
            Action action = behaviour.getAction(this, map);
            if (action != null)
                return action;
        }

        return new DoNothingAction();
    }

    /**
     *  let enemies try to follow and attack player
     */
    public void toAggressive(Actor target){
        this.behaviours.put(5, new FollowBehaviour(target));
        this.behaviours.put(4, new AttackBehaviour(target));
        this.behaviours.remove(2);
    }

    /**
     * make a dormant enemies should do nothing
     */
    public void becomeDormant(){
        this.behaviours.clear();
    }

    public void setDefaultChar() {
        setDisplayChar(defaultChar);
    }

    public void setMaskedChar() {
        setDisplayChar(Maskable.fogChar);
    }

    @Override
    public void resetInstance(Actor actor, GameMap map) {
        this.behaviours.clear();
        map.removeActor(this);
    }

    @Override
    public void registerInstance() {
        Resettable.super.registerInstance();
    }
}
