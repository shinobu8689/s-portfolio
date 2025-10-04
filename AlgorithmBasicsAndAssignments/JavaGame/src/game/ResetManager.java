package game;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.GameMap;

import java.util.ArrayList;
import java.util.List;

/**
 * A global Singleton manager that does soft-reset on the instances.
 * HINT: refer to Bootcamp Week 5 about static factory method.
 * A3: Think about how will you improve this implementation in the future assessment.
 * What could be the drawbacks of this implementation?
 */
public class ResetManager {
    /**
     * A list of resettable instances (any classes that implements Resettable,
     * such as Player implements Resettable will be stored in here)
     */
    private List<Resettable> resettableList;

    /**
     * A singleton reset manager instance
     */
    private static ResetManager instance;

    /**
     * Get the singleton instance of reset manager
     * @return ResetManager singleton instance
     */
    public static ResetManager getInstance(){
        if(instance == null){
            instance = new ResetManager();
        }
        return instance;
    }

    /**
     * Constructor
     */
    private ResetManager(){
        resettableList = new ArrayList<>();
    }

    /**
     * Reset the game by traversing through all the list
     * By doing this way, it will avoid using `instanceof` all over the place.
     */
    public void run(Actor actor, GameMap map){
        for (Resettable resettable : resettableList){
            resettable.resetInstance(actor, map);
        }
    }

    /**
     * Add the Resettable instance to the list
     *
     */
    public void appendResetInstance(Resettable resettable){
        resettableList.add(resettable);
    }


    /**
     * Remove a Resettable instance from the list
     * @param resettable resettable object
     *
     */
    public void cleanUp(Resettable resettable){
        resettableList.remove(resettable);
    }

}
