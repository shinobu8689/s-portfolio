package game.player;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;

/**
 * Manages the lives of the player
 *
 * @author Nethmini Botheju
 * @version 1.0
 */
public class Lives {
    private int lives;

    /**
     * constructor for the players lives
     *
     * @param lives an integer of the lives
     */
    public Lives(int lives) {
        this.lives = lives;
    }

    /**
     * Method that decreases the lives of the player
     */
    public void loseLife(){
        this.lives = this.lives - 1;
    }

    /**
     * The display for the lives on the output console
     *
     * @return a string of the hearts
     */
    public String getLivesStr(){
        if(this.lives == 4) {
            return "❤ ❤ ❤ ❤";
        }
        else if(this.lives == 3) {
            return "❤ ❤ ❤";
        }
        else if(this.lives == 2){
            return "❤ ❤";
        } else{
            return "️❤";
        }
    }

    /**
     * Checks if the player is still conscious to allow for a replay
     *
     * @param actor the actor that can replay
     * @param map the map which the game restarts on
     * @return boolean true or false
     */
    public boolean checksLives(Actor actor, GameMap map){
        if (!(actor.isConscious()) && this.lives > 1){
            return true;
        } else if(!(actor.isConscious()) && this.lives == 1){
            map.removeActor(actor);
        }
        return false;
    }

}
