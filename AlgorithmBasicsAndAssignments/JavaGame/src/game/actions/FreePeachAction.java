package game.actions;

import edu.monash.fit2099.engine.actions.Action;
import edu.monash.fit2099.engine.positions.GameMap;
import edu.monash.fit2099.engine.actors.Actor;

public class FreePeachAction extends Action {
    /**
     * Class for the action of freeing peach and ending the game
     */
    public FreePeachAction() {
    }

    @Override
    /**
     * The actual freeing and talking to peach part. Also removes the player from the 
     * game map, effectively ending the game.
     * @param actor the plaer
     * @param map the game map
     * @return Peach's thankful monologue
     */
    public String execute(Actor actor, GameMap map) {
        String thankfulPeach = "Thank you, but our Princess is in another castle! Just kidding!";
        map.removeActor(actor);
        return thankfulPeach;
    }

    @Override
    public String menuDescription(Actor actor) {
        return actor + " uses the key to free Princess Peach!";
    }
}
