package game.world;

import edu.monash.fit2099.engine.actors.Actor;
import edu.monash.fit2099.engine.positions.Ground;
import edu.monash.fit2099.engine.positions.Location;
import game.Status;

public class Fire extends BaseGround {
    /**
     * A class representing some hot ground, but not as hot as lava
     */
    private int age;

    public Fire() {
        super('v');
        this.age = 0;
    }

    @Override
    /**
     * Lets fire experience the flow of time. 
     * It will burn out after 3 turns, and will hurt any actor on top of it
     * @param location location of fire
     */
    public void tick(Location location) {
        this.age++;
        if (location.containsAnActor()) {
            Actor actor = location.getActor();
            if (!actor.hasCapability(Status.INVINCIBLE)){
                actor.hurt(20); // A bit too hot to stand on...
            }
        }

        if (this.age > 3) {
            // Once the fire is over 3 turns old, it burns itself out
            location.setGround(new Dirt());
        }
    }
}
