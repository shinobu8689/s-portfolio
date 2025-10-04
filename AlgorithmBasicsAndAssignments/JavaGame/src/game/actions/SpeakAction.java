package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;
import game.Status;
import game.Utils;

/**
 * Allows toad to print random speeches onto the console
 *
 * @author Nethmini Botheju
 * @version 1.0
 * @see edu.monash.fit2099.engine.actions.Action
 */
public class SpeakAction extends Action {

    /**
     * Class to output the monologue toad outputs when spoken to
     *
     * @param num random number between 1-4
     * @return string for each monologue Toad speaks
     */
    public String talk(int num) {
        return switch (num) {
            case 0 -> "You might need a wrench to smash Koopa's hard shells.";
            case 1 -> "You better get back to finding the Power Stars.";
            case 2 -> "The Princess is depending on you! You are our only hope.";
            case 3 -> "Being imprisoned in these walls can drive a fungus crazy :(";
            default -> null;
        };
    }

    /**
     * Perform the action of Toad speaking random monologues when Player interacts with him
     *
     * @param actor The actor performing the action.
     * @param map The map the actor is on.
     * @return a string of random speech
     */
    @Override
    public String execute(Actor actor, GameMap map) {
        int num = Utils.randomIntSpeech();
        if (actor.hasCapability(Status.INVINCIBLE) && actor.getWeapon().toString().equals("Wrench")) {
            while (num == 0 || num == 1) {
                num = Utils.randomIntSpeech();
            }
            return this.talk(num);
        } else if (actor.hasCapability(Status.INVINCIBLE)) {
            while (num == 1) {
                num = Utils.randomIntSpeech();
            }
            return this.talk(num);
        } else if (actor.getWeapon().toString().equals("Wrench")) {
            while (num == 0) {
                num = Utils.randomIntSpeech();
            }
            return this.talk(num);
        } else {
            return this.talk(num);
        }
    }

    /**
     * Returns a descriptive for user to prompt player speak to Toad
     *
     * @param actor The actor speaking to Toad
     * @return the text for player speak to Toad
     */
    @Override
    public String menuDescription(Actor actor) {
        return actor + " Speaks to Toad";
    }
}
