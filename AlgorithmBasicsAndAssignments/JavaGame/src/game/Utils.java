package game;

import edu.monash.fit2099.engine.positions.Location;
import game.actions.SpeakAction;

/**
 * Abstract class for creating random integers for chance based actions
 *
 * @author Nethmini Botheju
 * @version 1.0
 * @see game.items.Coin
 * @see SpeakAction
 */
public abstract class Utils {

    /**
     * Generates a random number from 1-4 for toad's speak action
     *
     * @return integer between 1 and 4 inclusive
     */
    public static int randomIntSpeech(){
        int num = (int) ((Math.random() * (1000 - 1)) + 1);
        return num % 4;
    }

    /**
     * Generates a random number from 1 and 500 inclusive for the value of coins
     *
     * @return integer between 1 and 500 inclusive that is divisible by 5
     */
    public static int randomIntCoin(){
        int num = (int) ((Math.random() * (500 - 1)) + 1);
        while (num % 5 != 0){
            num = (int) ((Math.random() * (500 - 1)) + 1);
        }
        return num;
    }
    /**
     * Returns a boolean with @param percentage chance of being true
     *
     * @param percentage chance that true is returned
     * @return boolean
     */
    public static boolean randomChance(int percentage) {
        int num = (int) ((Math.random() * (100 - 1)) + 1);

        if (num <= percentage) {
            return true;
        }
        else {
            return false;
        }
    }
    /**
     * Returns a random integer between [0, range]
     *
     * @param range max num of elements
     * @return random int
     */
    public static int randomPick(int range) {
        int num = (int) (Math.random() * (range - 1));
        return num;
    }

    /**
     * Compute the Manhattan distance between two locations.
     *
     * @param a the first location
     * @param b the first location
     * @return the number of steps between a and b if you only move in the four cardinal directions.
     */
    public static int distance(Location a, Location b) {
        return Math.abs(Math.abs(a.x() - b.x()) + Math.abs(a.y() - b.y()));
    }
}
