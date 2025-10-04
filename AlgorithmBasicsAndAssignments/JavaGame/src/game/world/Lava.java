package game.world;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;
import game.player.Player;

/**
 * Class for the lava ground
 * @author Neth Botheju
 * @version 1.0
 */
public class Lava extends BaseGround{
    /**
     * Constructor.
     */
    public Lava() {
        super('L');
    }

    /**
     * determines if the actor is a player to enter
     *
     * @param actor the Actor to check
     * @return true or false if the actor can step on the lava
     */
    public boolean canActorEnter(Actor actor) {
        if (actor instanceof Player){
            return true;
        } else {
            return false;
        }
    }

    /**
     * Causes damage to the actor if stepped on
     *
     * @param location The location of the Ground
     */
    @Override
    public void tick(Location location){
        super.tick(location);
        if (location.containsAnActor()){
            Player actor = (Player) location.getActor();
            if (!actor.hasCapability(Status.INVINCIBLE)){
                actor.hurt(15);
                actor.getBurnt();
                actor.getLives().checksLives(actor,location.map());
            }
        }
    }
}
